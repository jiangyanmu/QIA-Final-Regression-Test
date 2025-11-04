# 出場函數
def outp(df, r, b, price_col, i):
    r = r + b * df.iloc[i][price_col]
    df.loc[i, "ret"] = r
    r = 0
    b = 0
    return (r, b)


# 進場函數
def inp(df, r, b, i):
    df.loc[i, "sign"] = b
    r = r - b * df.iloc[i]["開盤價"]
    return (r, b)
