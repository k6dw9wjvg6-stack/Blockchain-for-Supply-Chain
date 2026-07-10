import os
import pandas as pd
def generate_descriptive_stats(input_path: str) -> None:
    """读取结果数据并打印/保存描述性统计信息。"""
    if not os.path.exists(input_path):
        print(f"Error: {input_path} 不存在，请先运行 calculate_re.py")
        return
    df = pd.read_excel(input_path)
    print("\n" + "=" * 20 + " 数据的描述性统计报告 " + "=" * 20)
    stats = df.describe()
    print(stats)
    print("=" * 60 + "\n")
    # 推荐：顺便把统计结果保存下来，方便在 GitHub 仓库或论文中引用
    stats_output_path = os.path.join("output", "tables", "descriptive_stats.csv")
    os.makedirs(os.path.dirname(stats_output_path), exist_ok=True)
    stats.to_csv(stats_output_path)
    print(f"统计报告已额外保存为 CSV 方便查看: {stats_output_path}")
if __name__ == "__main__":
    RESULT_FILE = os.path.join("output", "tables", "result.xlsx")
    generate_descriptive_stats(RESULT_FILE)
