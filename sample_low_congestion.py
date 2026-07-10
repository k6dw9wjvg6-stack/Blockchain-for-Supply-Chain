import os
import pandas as pd
def sample_low_congestion(input_path: str, output_path: str, target_n: int = 2950) -> None:
    """对低拥堵数据进行概率抽样。"""
    if not os.path.exists(input_path):
        print(f"❌ 错误: 找不到输入文件 {input_path}")
        return
    print(f"正在读取低拥堵数据: {input_path}")
    df = pd.read_excel(input_path, engine="openpyxl")
    print("📊 原始总数据量:", len(df))
    time_col = "block_time"
    if time_col not in df.columns:
        raise ValueError(f"❌ 核心错误: 数据中找不到 '{time_col}' 列")
    # 计算概率权重
    weights = df[time_col].value_counts(normalize=True)
    df["_weight"] = df[time_col].map(weights)
    df["_weight"] = df["_weight"] / df["_weight"].sum()
    # 随机抽样
    sample_size = min(target_n, len(df))
    df_sampled = df.sample(n=sample_size, weights="_weight", random_state=42)
    df_sampled = df_sampled.drop(columns=["_weight"])
    # 自动保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_sampled.to_excel(output_path, index=False, engine="openpyxl")
    print("\n🎉 抽样完成！")
    print("💾 抽样后文件已保存至:", output_path)
    print("📊 最终行数:", len(df_sampled))
if __name__ == "__main__":
    # 使用相对路径，方便 GitHub 协同开发
    INPUT_FILE = os.path.join("data", "raw", "低拥堵B1.xlsx")
    OUTPUT_FILE = os.path.join("data", "cleaned", "低拥堵B1_2950_分层抽样.xlsx")
    sample_low_congestion(INPUT_FILE, OUTPUT_FILE)
