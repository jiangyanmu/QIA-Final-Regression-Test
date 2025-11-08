from lib.technical_indicators import calc_ma

def backtest_strategy_two(df, short_ma_period=5, long_ma_period=20):
    df = df.copy()
    # 1. 計算所需指標
    df = calc_ma(df, period=short_ma_period)
    df = calc_ma(df, period=long_ma_period)

    short_ma_col = f'MA{short_ma_period}'
    long_ma_col = f'MA{long_ma_period}'

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
    for i in range(1, L): # 從第二天開始，因為需要前一天的訊號
        idx = df.index[i]
        prev_row = df.iloc[i-1]
        row = df.iloc[i]

        # --- 進場邏輯 (使用前一天的訊號，今天開盤進場) ---
        if position == 0 and i > 1: # 需要i-2的資料，所以從i>1開始判斷
            prev_prev_row = df.iloc[i-2]
            # 檢查前一天是否發生黃金交叉
            if prev_prev_row[short_ma_col] < prev_prev_row[long_ma_col] and prev_row[short_ma_col] > prev_row[long_ma_col]:
                # 今天開盤進場
                avg_cost = row["開盤價"]
                position = 1
        
        # --- 出場邏輯 (當日判斷，當日收盤出場) ---
        if position == 1:
            mid_price = (row["開盤價"] + row["收盤價"]) / 2
            if mid_price < row[short_ma_col]:
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
