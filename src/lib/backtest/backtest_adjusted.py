import numpy as np
from tqdm.notebook import tqdm
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

def sensitivity_analysis_one(
    df_original,
    backtest_func,
    performance_func,
    param_ranges=None,
    iterations=100
):
    """
    通用敏感度分析函數 (適用於策略一)

    Parameters
    ----------
    df_original : pd.DataFrame
        原始資料
    backtest_func : function
        回測策略函數，需接受 df 和參數
    performance_func : function
        計算績效函數，接受回測結果 df，返回 dict
    param_ranges : dict
        參數範圍，例如：
        {
            'ma_period': (3, 15),
            'bb_period': (16, 40),
            'bb_std': (1.0, 3.0),
            'drop_threshold': (0.1, 0.9)
        }
    iterations : int
        隨機測試次數

    Returns
    -------
    results_df : pd.DataFrame
        所有回測結果
    """

    if param_ranges is None:
        param_ranges = {
            'ma_period': (3, 15),
            'bb_period': (16, 40),
            'bb_std': (1.0, 3.0),
            'drop_threshold': (0.1, 0.9)
        }

    results_list = []
    print(f"準備進行 {iterations} 次隨機參數測試...")

    for _ in tqdm(range(iterations), desc="執行進度"):
        # 隨機生成參數
        ma_p = random.randint(*param_ranges['ma_period'])
        bb_p = random.randint(*param_ranges['bb_period'])
        while bb_p <= ma_p:
            bb_p = random.randint(*param_ranges['bb_period'])
        bb_s = random.uniform(*param_ranges['bb_std'])
        drop_t = random.uniform(*param_ranges['drop_threshold'])

        # 回測
        df_result = backtest_func(
            df_original.copy(),
            ma_period=ma_p,
            bb_period=bb_p,
            bb_std=bb_s,
            drop_threshold=drop_t
        )

        # 計算績效
        df_result['entry'] = (df_result['position'] == 1) & (df_result['position'].shift(1) == 0)
        df_result['exit'] = (df_result['position'] == 0) & (df_result['position'].shift(1) == 1)
        performance = performance_func(df_result)

        # 儲存結果
        run_results = {
            'ma_period': ma_p,
            'bb_period': bb_p,
            'bb_std': round(bb_s, 2),
            'drop_threshold': round(drop_t, 2)
        }
        run_results.update(performance)
        results_list.append(run_results)

    results_df = pd.DataFrame(results_list)

    return results_df

def sensitivity_analysis_three(
    df_original,
    backtest_func,
    performance_func,
    param_ranges,
    iterations=100
):
    """
    敏感度分析函數 (適用於策略二)
    """
    results_list = []
    print(f"準備進行 {iterations} 次隨機參數測試...")

    for _ in tqdm(range(iterations), desc="執行進度"):
        # 隨機生成參數
        short_ma = random.randint(*param_ranges['short_ma_period'])
        long_ma = random.randint(*param_ranges['long_ma_period'])
        while short_ma >= long_ma:
            short_ma = random.randint(*param_ranges['short_ma_period'])
            long_ma = random.randint(*param_ranges['long_ma_period'])

        # 回測
        df_result = backtest_func(
            df_original.copy(),
            short_ma_period=short_ma,
            long_ma_period=long_ma
        )

        # 計算績效
        df_result['entry'] = (df_result['position'] == 1) & (df_result['position'].shift(1) == 0)
        df_result['exit'] = (df_result['position'] == 0) & (df_result['position'].shift(1) == 1)
        performance = performance_func(df_result)

        # 儲存結果
        run_results = {
            'short_ma_period': short_ma,
            'long_ma_period': long_ma,
        }
        run_results.update(performance)
        results_list.append(run_results)

    results_df = pd.DataFrame(results_list)
    return results_df

def sensitivity_analysis_two(
    df_original,
    backtest_func,
    performance_func,
    param_ranges,
    iterations=100
):
    """
    敏感度分析函數 (適用於策略二)
    """
    results_list = []
    print(f"準備進行 {iterations} 次隨機參數測試...")

    for _ in tqdm(range(iterations), desc="執行進度"):
        # 隨機生成參數
        short_ma = random.randint(*param_ranges['short_ma_period'])
        long_ma = random.randint(*param_ranges['long_ma_period'])
        while short_ma >= long_ma:
            short_ma = random.randint(*param_ranges['short_ma_period'])
            long_ma = random.randint(*param_ranges['long_ma_period'])

        # 回測
        df_result = backtest_func(
            df_original.copy(),
            short_ma_period=short_ma,
            long_ma_period=long_ma
        )

        # 計算績效
        df_result['entry'] = (df_result['position'] == 1) & (df_result['position'].shift(1) == 0)
        df_result['exit'] = (df_result['position'] == 0) & (df_result['position'].shift(1) == 1)
        performance = performance_func(df_result)

        # 儲存結果
        run_results = {
            'short_ma_period': short_ma,
            'long_ma_period': long_ma,
        }
        run_results.update(performance)
        results_list.append(run_results)

    results_df = pd.DataFrame(results_list)
    return results_df

def sensitivity_analysis_three(
    df_original,
    backtest_func,
    performance_func,
    param_ranges,
    iterations=100
):
    """
    敏感度分析函數 (適用於策略三)
    """
    results_list = []
    print(f"準備進行 {iterations} 次隨機參數測試...")

    for _ in tqdm(range(iterations), desc="執行進度"):
        # 隨機生成參數
        ma_s = random.randint(*param_ranges['ma_short'])
        ma_m = random.randint(*param_ranges['ma_medium'])
        ma_l = random.randint(*param_ranges['ma_long'])
        while not (ma_s < ma_m < ma_l):
            ma_s = random.randint(*param_ranges['ma_short'])
            ma_m = random.randint(*param_ranges['ma_medium'])
            ma_l = random.randint(*param_ranges['ma_long'])

        # 回測
        df_result = backtest_func(
            df_original.copy(),
            ma_short=ma_s,
            ma_medium=ma_m,
            ma_long=ma_l
        )

        # 計算績效
        df_result['entry'] = (df_result['position'] == 1) & (df_result['position'].shift(1) == 0)
        df_result['exit'] = (df_result['position'] == 0) & (df_result['position'].shift(1) == 1)
        performance = performance_func(df_result)

        # 儲存結果
        run_results = {
            'ma_short': ma_s,
            'ma_medium': ma_m,
            'ma_long': ma_l,
        }
        run_results.update(performance)
        results_list.append(run_results)

    results_df = pd.DataFrame(results_list)
    return results_df

def plot_strategy_sensitivity(
    results_df: pd.DataFrame,
    equity_col: str = '最終權益 (Mark-to-Market)',
    param_cols: list = ['ma_period', 'bb_period', 'bb_std', 'drop_threshold'],
    group_labels: list = ['低績效', '中績效', '高績效'],
    hist_bins: int = 20,
    palette: list = ['#1f77b4', '#ff7f0e', '#2ca02c'],
    subplot_shape: tuple = (2, 2)
):
    """
    繪製策略參數敏感度分析圖表（第二張圖固定箱型圖）

    params:
        results_df : pd.DataFrame 包含回測結果與策略參數
        equity_col : str 績效欄位名稱
        param_cols : list[str] 需要分析的策略參數欄位
        group_labels: list[str] 分區標籤
        hist_bins   : int 直方圖 bins 數
        palette     : list 顏色列表
        subplot_shape: tuple (rows, cols) 決定箱型圖的排列方式
    """
    if results_df.empty:
        print("results_df 為空，無法分析。")
        return

    # 設定中文字型與負號
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 1️⃣ 將績效分組
    results_df['equity_group'] = pd.qcut(
        results_df[equity_col],
        q=3,
        labels=group_labels
    )

    # 2️⃣ 繪製彩色直方圖
    plt.figure(figsize=(10, 5))
    sns.histplot(
        data=results_df,
        x=equity_col,
        hue='equity_group',
        bins=hist_bins,
        palette=palette,
        multiple='stack',
        edgecolor='black',
        alpha=0.8
    )
    plt.title(f'{equity_col} 分布（按績效區間分色）', fontsize=16)
    plt.xlabel(equity_col)
    plt.ylabel('頻率')
    plt.grid(True)
    plt.show()

    # 3️⃣ 計算中位數並顯示
    median_table = results_df.groupby('equity_group', observed=True)[param_cols].median()
    print("不同績效區間的策略參數中位數：")
    display(median_table)

    # 4️⃣ 繪製箱型圖
    n_rows, n_cols = subplot_shape
    total_plots = n_rows * n_cols

    # 若格子太少，自動調整為一列多圖
    if total_plots < len(param_cols):
        n_rows = 1
        n_cols = len(param_cols)
        print(f"⚠️ subplot_shape 不足，已自動改為 ({n_rows}, {n_cols})")

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
    fig.suptitle(f'{equity_col} 區間策略參數分布（箱型圖）', fontsize=20)

    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for i, param in enumerate(param_cols):
        ax = axes[i]
        sns.boxplot(
            data=results_df,
            x='equity_group',
            y=param,
            hue='equity_group',
            ax=ax,
            palette=palette,
            width=0.5,
            dodge=False,
            legend=False
        )
        ax.set_title(f'{param} 在不同績效區間的分布', fontsize=14)
        ax.set_xlabel('最終權益區間', fontsize=12)
        ax.set_ylabel(param, fontsize=12)
        ax.grid(True)

        # 🔹 自動調整 Y 軸格式：整數或最多兩位小數
        y_min, y_max = results_df[param].min(), results_df[param].max()
        if abs(y_max - y_min) > 10:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))
        else:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
