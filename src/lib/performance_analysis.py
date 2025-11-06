import pandas as pd


# 計算策略績效
def result_F(df):
    last = df["cus"].iloc[-1]
    count = df["sign"][df["sign"] != 0].count()

    def maxdrawdown(s):
        s = s.cummax() - s
        return s.max()

    mdd = maxdrawdown(df["cus"])
    w = df["ret"][df["ret"] > 0].count() / count if count > 0 else 0
    result = pd.DataFrame(
        {"最後報酬": [last], "交易次數": [count], "最大回損": [mdd], "勝率": [w]}
    )
    return result


def calculate_strategy_one_performance(df_backtest_output: pd.DataFrame) -> dict:
    """
    從 backtest_strategy 函數的輸出 DataFrame 中計算詳細的績效指標。

    Args:
        df_backtest_output (pd.DataFrame):
            已經執行過 backtest_strategy 的回測結果 DataFrame，
            必須包含以下欄位：
            - 'ret': 每筆交易的已實現報酬（進場為 0，出場時記錄盈虧）
            - 'cus': 累積市值權益曲線（Mark-to-Market 權益）

    Returns:
        dict: 包含 16 項策略績效指標的字典，適用於交易策略評估與報告。
    """

    # === 步驟 1：提取已實現的交易盈虧（一進一出完成的交易）===
    # 'ret' 欄位中非零值代表「完成一筆交易」的實際損益
    # dropna() 確保移除任何可能的 NaN
    trades = df_backtest_output["ret"][df_backtest_output["ret"] != 0].dropna()

    # === 步驟 2：提取累積權益曲線，用於計算最大回撤 ===
    cus_series = df_backtest_output["cus"]

    # === 內部函數：計算最大回撤 (Maximum Drawdown, MDD) ===
    def maxdrawdown(s: pd.Series) -> float:
        """
        計算權益曲線的最大回撤。
        公式：當前最高點 - 當前權益 的最大值
        """
        peak = s.cummax()  # 到目前為止的最高權益
        drawdown = peak - s  # 每期的回撤金額
        return drawdown.max()  # 最大回撤值

    mdd = maxdrawdown(cus_series)

    # === 步驟 3：計算總交易次數 ===
    total_trades = len(trades)

    # === 特殊情況：若策略完全沒有交易，避免除以 0 錯誤 ===
    if total_trades == 0:
        return {
            "最終權益 (Mark-to-Market)": (
                cus_series.iloc[-1] if not cus_series.empty else 0
            ),  # 若有持倉，顯示最終市值；否則為 0
            "淨利或淨損 (已實現)": 0,
            "最大回撤 (MDD)": mdd,
            "總交易次數": 0,
            "勝率": "0.00%",
            "總獲利 (已實現)": 0,
            "總損失 (已實現)": 0,
            "賺錢交易次數": 0,
            "虧錢交易次數": 0,
            "單次交易最大獲利": 0,
            "單次交易最大損失": 0,
            "獲利交易中的平均獲利": 0,
            "損失交易中的平均損失": 0,
            "賺賠比": 0,
            "最長的連續性獲利的次數": 0,
            "最長的連續性損失的次數": 0,
        }

    # === 步驟 4：分類獲利與虧損交易 ===
    winning_trades = trades[trades > 0]  # 賺錢的交易
    losing_trades = trades[trades < 0]  # 虧錢的交易

    # === 步驟 5：計算總獲利與總損失 ===
    total_profit = winning_trades.sum()  # 所有正報酬加總
    total_loss = losing_trades.sum()  # 所有負報酬加總（結果為負）

    # === 步驟 6：交易次數統計 ===
    num_winning_trades = len(winning_trades)
    num_losing_trades = len(losing_trades)

    # === 步驟 7：勝率計算（格式化為百分比）===
    win_rate = num_winning_trades / total_trades

    # === 步驟 8：單筆極值 ===
    max_profit_trade = winning_trades.max() if not winning_trades.empty else 0
    max_loss_trade = (
        losing_trades.min() if not losing_trades.empty else 0
    )  # 最小值即最大損失

    # === 步驟 9：平均獲利與平均損失 ===
    avg_profit = total_profit / num_winning_trades if num_winning_trades > 0 else 0
    avg_loss = total_loss / num_losing_trades if num_losing_trades > 0 else 0  # 負值

    # === 步驟 10：賺賠比（Profit Factor）===
    # 平均獲利 / |平均損失|，若無虧損則為無窮大
    if avg_loss == 0:
        profit_loss_ratio = float("inf")
    else:
        profit_loss_ratio = abs(avg_profit / avg_loss)

    # === 步驟 11：計算最長連勝與最長連輸（Streak Analysis）===
    longest_win_streak = longest_loss_streak = 0
    current_win_streak = current_loss_streak = 0

    for trade_return in trades:
        if trade_return > 0:
            current_win_streak += 1
            current_loss_streak = 0
        elif trade_return < 0:
            current_loss_streak += 1
            current_win_streak = 0

        # 更新歷史最長紀錄
        longest_win_streak = max(longest_win_streak, current_win_streak)
        longest_loss_streak = max(longest_loss_streak, current_loss_streak)

    # === 步驟 12：組裝並回傳績效指標字典 ===
    metrics = {
        "最終權益 (Mark-to-Market)": cus_series.iloc[
            -1
        ],  # 回測結束時的總資產（含未平倉）
        "淨利或淨損 (已實現)": trades.sum(),  # 所有已實現交易的淨損益
        "最大回撤 (MDD)": mdd,  # 權益曲線最大跌幅
        "總獲利 (已實現)": total_profit,  # 所有賺錢交易總和
        "總損失 (已實現)": total_loss,  # 所有虧錢交易總和（負數）
        "總交易次數": total_trades,  # 進出場總次數
        "賺錢交易次數": num_winning_trades,  # 獲利交易筆數
        "虧錢交易次數": num_losing_trades,  # 虧損交易筆數
        "勝率": f"{win_rate:.2%}",  # 勝率（例如：66.67%）
        "單次交易最大獲利": max_profit_trade,  # 單筆最高獲利
        "單次交易最大損失": max_loss_trade,  # 單筆最大損失
        "獲利交易中的平均獲利": avg_profit,  # 每次贏平均賺多少
        "損失交易中的平均損失": avg_loss,  # 每次輸平均虧多少（負值）
        "賺賠比": profit_loss_ratio,  # 平均獲利 / |平均損失|
        "最長的連續性獲利的次數": longest_win_streak,  # 最大連勝次數
        "最長的連續性損失的次數": longest_loss_streak,  # 最大連輸次數
    }

    return metrics
