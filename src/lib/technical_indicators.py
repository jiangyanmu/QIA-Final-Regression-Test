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
