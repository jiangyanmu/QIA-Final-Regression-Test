# 回測策略三: 裸K (均線排列)
from lib.technical_indicators import calc_MA3, calc_MA5, calc_MA10


def backtest_strategy_three(df):
    df = df.copy()
    # 1. 計算所需指標
    df = calc_MA3(df)
    df = calc_MA5(df)
    df = calc_MA10(df)

    L = len(df)
    if L < 2:
        return df

    # 2. 初始化欄位
    df["ret"] = 0.0
    df["cus"] = 0.0
    df["position"] = 0

    position = 0
    avg_cost = 0.0
    cum_ret = 0.0

    # 3. 遍歷所有交易日
    for i in range(1, L):  # 從第二天開始，因為需要前一天的訊號
        idx = df.index[i]
        prev_row = df.iloc[i - 1]
        row = df.iloc[i]

        # --- 進場邏輯 (使用前一天的訊號，今天開盤進場) ---
        if position == 0:
            # 檢查前一天的進場條件: 均線多頭排列
            if prev_row["MA3"] > prev_row["MA5"] and prev_row["MA5"] > prev_row["MA10"]:
                # 今天開盤進場
                avg_cost = row["開盤價"]
                position = 1

        # --- 出場邏輯 (當日判斷，當日收盤出場) ---
        if position == 1:
            # 檢查出場條件: 3日均線下穿5日均線
            if row["MA3"] < row["MA5"]:
                exit_price = row["收盤價"]
                ret = exit_price - avg_cost
                df.at[idx, "ret"] = ret
                cum_ret += ret
                position = 0
                avg_cost = 0.0

        # --- 計算浮動盈虧 ---
        if position == 1:
            df.at[idx, "cus"] = cum_ret + (row["收盤價"] - avg_cost)
        else:
            df.at[idx, "cus"] = cum_ret

        # --- 記錄持倉 ---
        df.at[idx, "position"] = position

    # --- Buy & Hold ---
    df["BH"] = df["收盤價"] - df["收盤價"].iloc[0]

    return df
