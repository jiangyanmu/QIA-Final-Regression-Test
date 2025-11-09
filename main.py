import pandas as pd
from lib.backtest.backtest_adjusted import sensitivity_analysis_two, sensitivity_analysis_three
from lib.backtest.strategy_two import backtest_strategy_two
from lib.backtest.strategy_three import backtest_strategy_three
from lib.performance_analysis import calculate_strategy_one_performance

def run_strategy_two_analysis(df_original):
    """
    對策略二進行敏感度分析
    """
    print("--- 開始執行策略二(模組二)敏感度分析 ---")
    param_ranges = {
        'short_ma_period': (3, 10),
        'long_ma_period': (15, 30)
    }
    results_df = sensitivity_analysis_two(
        df_original=df_original,
        backtest_func=backtest_strategy_two,
        performance_func=calculate_strategy_one_performance,
        param_ranges=param_ranges,
        iterations=100  # 為了快速演示，減少迭代次數
    )
    print("策略二分析完成。")
    print("分析結果預覽:")
    print(results_df.head())
    print("\n最佳結果 (依據最終權益):")
    print(results_df.sort_values(by='最終權益 (Mark-to-Market)', ascending=False).head())
    print("-" * 40)
    return results_df

def run_strategy_three_analysis(df_original):
    """
    對策略三進行敏感度分析
    """
    print("\n--- 開始執行策略三(模組三)敏感度分析 ---")
    param_ranges = {
        'ma_short': (3, 8),
        'ma_medium': (9, 15),
        'ma_long': (16, 30)
    }
    results_df = sensitivity_analysis_three(
        df_original=df_original,
        backtest_func=backtest_strategy_three,
        performance_func=calculate_strategy_one_performance,
        param_ranges=param_ranges,
        iterations=100  # 為了快速演示，減少迭代次數
    )
    print("策略三分析完成。")
    print("分析結果預覽:")
    print(results_df.head())
    print("\n最佳結果 (依據最終權益):")
    print(results_df.sort_values(by='最終權益 (Mark-to-Market)', ascending=False).head())
    print("-" * 40)
    return results_df

if __name__ == '__main__':
    try:
        # main.py 位於根目錄，所以路徑是 'data/...'
        df = pd.read_csv("data/TPE-sample1.csv", encoding="utf-8")
        print(f"資料載入成功，共 {len(df)} 筆。")

        # 執行策略二分析
        strategy_two_results = run_strategy_two_analysis(df.copy())

        # 執行策略三分析
        strategy_three_results = run_strategy_three_analysis(df.copy())

    except FileNotFoundError:
        print("錯誤：找不到資料檔案 'data/TPE-sample1.csv'。請確認檔案路徑是否正確。")
    except Exception as e:
        print(f"執行時發生錯誤: {e}")