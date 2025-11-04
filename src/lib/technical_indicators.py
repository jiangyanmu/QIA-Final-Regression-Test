# 計算 MA
def MA(s, l, df):
    df["ma_s"] = df["收盤價"].rolling(s).mean()
    df["ma_l"] = df["收盤價"].rolling(l).mean()
    df["ma_sign"] = 0
    df.loc[
        (df["ma_s"].shift(1) < df["ma_l"].shift(1)) & (df["ma_s"] >= df["ma_l"]),
        "ma_sign",
    ] = 1
    df.loc[
        (df["ma_s"].shift(1) > df["ma_l"].shift(1)) & (df["ma_s"] <= df["ma_l"]),
        "ma_sign",
    ] = -1


# 計算 RSI
def RSI(d, df):
    x = df["收盤價"].diff()
    epsilon = 1e-10
    df["rsi"] = (
        100
        * x.where(x > 0, 0).rolling(d).mean()
        / (x.where(x > 0, -x).rolling(d).mean() + epsilon)
    )
    df["rsi_sign"] = 0
    df.loc[df["rsi"] < 20, "rsi_sign"] = 1
    df.loc[df["rsi"] > 80, "rsi_sign"] = -1


# 1️⃣ 五日均線
def calc_MA5(df, period=5):
    """
    計算五日均線
    """
    df["MA5"] = df["收盤價"].rolling(period).mean()
    return df


# 2️⃣ 布林軌道
def calc_Bollinger(df, n=20, k=2):
    """
    計算布林帶
    """
    df["BB_MA"] = df["收盤價"].rolling(n).mean()
    df["BB_STD"] = df["收盤價"].rolling(n).std()
    df["BB_Upper"] = df["BB_MA"] + k * df["BB_STD"]
    df["BB_Lower"] = df["BB_MA"] - k * df["BB_STD"]
    return df


# 3️⃣ 昨天漲幅
def calc_prev_gain(df):
    """
    計算昨天漲幅
    """
    df["prev_gain"] = (df["收盤價"] - df["收盤價"].shift(1)) / df["收盤價"].shift(1)
    return df
