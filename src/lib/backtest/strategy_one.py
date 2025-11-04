# 回測策略（隔天開盤進場版）
from lib.technical_indicators import calc_Bollinger, calc_MA5, calc_prev_gain


def backtest_strategy(df):
    df = df.copy()
    df = calc_MA5(df).copy()
    df = calc_Bollinger(df).copy()
    df = calc_prev_gain(df).copy()

    L = len(df)
    if L == 0:
        return df

    # 初始化欄位
    df["ret"] = 0.0
    df["cus"] = 0.0
    df["position"] = 0

    position = 0
    avg_cost = 0.0
    cum_ret = 0.0
    enter_signal = False  # 是否隔天要進場
    enter_price = 0.0  # 隔天開盤進場價格

    for i in range(L):
        idx = df.index[i]
        row = df.iloc[i]

        # --- 隔天開盤進場 ---
        if enter_signal:
            avg_cost = row["收盤價"]  # 假設開盤價與當日收盤價相同
            position = 1
            enter_signal = False
            # 如果你有真實開盤價欄位，可以用 row["開盤價"] 取代
            # avg_cost = row["開盤價"]

        # --- 出場條件（當日收盤） ---
        if position == 1 and row["收盤價"] < row["MA5"]:
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

        # --- 當日收盤判斷進場信號 ---
        if position == 0:
            if row["收盤價"] > row["BB_Upper"]:
                gain_yesterday = row.get("prev_gain", 0.0)
                # 隔天開盤價預測（可用 row["收盤價"] 或 next day open）
                if i + 1 < L:
                    next_open = df.iloc[i + 1]["收盤價"]  # 用開盤價更準確
                    if next_open >= row["收盤價"] - gain_yesterday / 2:
                        enter_signal = True
                        enter_price = next_open

    # --- Buy & Hold ---
    df["BH"] = df["收盤價"] - df["收盤價"].iloc[0]

    return df
