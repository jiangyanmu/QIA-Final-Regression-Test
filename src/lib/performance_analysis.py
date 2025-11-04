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


import pandas as pd


import pandas as pd


def calculate_strategy_performance(
    df: pd.DataFrame, price_col="close", entry_col="entry", exit_col="exit"
):
    """
    計算策略績效，只統計符合策略進出場條件的完整交易。

    Args:
        df (pd.DataFrame): 每日資料，需包含價格與策略訊號
            - price_col: 收盤價或成交價列名稱
            - entry_col: 進場訊號列名稱 (布林值 True/False)
            - exit_col: 出場訊號列名稱 (布林值 True/False)
        price_col, entry_col, exit_col: str，分別指定欄位名稱
    Returns:
        dict: 包含策略績效指標的字典
    """

    trade_returns = []  # 用來存放每筆完整交易的盈虧
    position_open = False
    entry_price = 0

    # 遍歷每日資料
    for i, row in df.iterrows():
        # 如果符合進場條件，且目前沒有持倉，進場
        if row[entry_col] and not position_open:
            position_open = True
            entry_price = row[price_col]

        # 如果符合出場條件，且目前有持倉，出場
        elif row[exit_col] and position_open:
            position_open = False
            exit_price = row[price_col]
            profit_loss = exit_price - entry_price  # 計算單筆交易盈虧
            trade_returns.append(profit_loss)

    # 如果最後一天仍有持倉，可選擇強制平倉或忽略
    # 這裡選擇忽略，因為策略未出場
    # if position_open:
    #     exit_price = df.iloc[-1][price_col]
    #     trade_returns.append(exit_price - entry_price)

    # 將完整交易盈虧轉成 Pandas Series
    trade_returns = pd.Series(trade_returns)

    # --- 以下套用你原本的績效函數計算 ---
    trades = trade_returns[trade_returns != 0].dropna()
    total_trades = len(trades)
    if total_trades == 0:
        return {
            "淨利或淨損": 0,
            "總獲利": 0,
            "總損失": 0,
            "總交易次數": 0,
            "賺錢交易次數": 0,
            "虧錢交易次數": 0,
            "勝率": "0.00%",
            "單次交易最大獲利": 0,
            "單次交易最大損失": 0,
            "獲利交易中的平均獲利": 0,
            "損失交易中的平均損失": 0,
            "賺賠比": 0,
            "最長的連續性獲利的次數": 0,
            "最長的連續性損失的次數": 0,
        }

    # 分別計算獲利交易與虧損交易
    winning_trades = trades[trades > 0]
    losing_trades = trades[trades < 0]

    total_profit = winning_trades.sum()
    total_loss = losing_trades.sum()
    num_winning_trades = len(winning_trades)
    num_losing_trades = len(losing_trades)

    win_rate = num_winning_trades / total_trades
    max_profit_trade = winning_trades.max() if not winning_trades.empty else 0
    max_loss_trade = losing_trades.min() if not losing_trades.empty else 0
    avg_profit = total_profit / num_winning_trades if num_winning_trades > 0 else 0
    avg_loss = total_loss / num_losing_trades if num_losing_trades > 0 else 0
    profit_loss_ratio = abs(avg_profit / avg_loss) if avg_loss != 0 else float("inf")

    # 計算最長連續獲利/虧損
    longest_win_streak = longest_loss_streak = 0
    current_win_streak = current_loss_streak = 0
    for trade_return in trades:
        if trade_return > 0:
            current_win_streak += 1
            current_loss_streak = 0
        elif trade_return < 0:
            current_loss_streak += 1
            current_win_streak = 0
        longest_win_streak = max(longest_win_streak, current_win_streak)
        longest_loss_streak = max(longest_loss_streak, current_loss_streak)

    metrics = {
        "淨利或淨損": trades.sum(),
        "總獲利": total_profit,
        "總損失": total_loss,
        "總交易次數": total_trades,
        "賺錢交易次數": num_winning_trades,
        "虧錢交易次數": num_losing_trades,
        "勝率": f"{win_rate:.2%}",
        "單次交易最大獲利": max_profit_trade,
        "單次交易最大損失": max_loss_trade,
        "獲利交易中的平均獲利": avg_profit,
        "損失交易中的平均損失": avg_loss,
        "賺賠比": profit_loss_ratio,
        "最長的連續性獲利的次數": longest_win_streak,
        "最長的連續性損失的次數": longest_loss_streak,
    }

    return metrics
