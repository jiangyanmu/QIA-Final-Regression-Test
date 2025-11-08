from lib.technical_indicators import calc_ma


def backtest_strategy_three(df, ma_short=3, ma_medium=5, ma_long=10):
    df = df.copy()
    # 1. 計算所需指標
    df = calc_ma(df, period=ma_short)
    df = calc_ma(df, period=ma_medium)
    df = calc_ma(df, period=ma_long)

    short_ma_col = f'MA{ma_short}'
    medium_ma_col = f'MA{ma_medium}'
    long_ma_col = f'MA{ma_long}'

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
            if prev_row[short_ma_col] > prev_row[medium_ma_col] and prev_row[medium_ma_col] > prev_row[long_ma_col]:
                # 今天開盤進場
                avg_cost = row["開盤價"]
                position = 1

        # --- 出場邏輯 (當日判斷，當日收盤出場) ---
        if position == 1:
            # 檢查出場條件: 3日均線下穿5日均線
            if row[short_ma_col] < row[medium_ma_col]:
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
