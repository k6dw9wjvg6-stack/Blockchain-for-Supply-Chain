import os
import pandas as pd


def clean_dataset(input_path: str, output_path: str) -> None:
    """读取原始燃气数据，清洗重复值、缺失值及异常负数，并保存结果。"""
    if not os.path.exists(input_path):
        print(f"Error: 找不到输入文件 {input_path}")
        return

    print(f"正在读取数据: {input_path}...")
    df = pd.read_excel(input_path)

    # 1. 去除完全重复的行
    df = df.drop_duplicates()

    # 2. 核心字段类型转换与清洗
    target_cols = ["Gas Price", "Gas Used"]
    for col in target_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. 剔除关键字段含空值的行
    required_cols = ["Timestamp"] + target_cols
    # 只检查实际存在的列，防止因列名对不上而报错
    existing_required = [c for c in required_cols if c in df.columns]
    df = df.dropna(subset=existing_required)

    # 4. 过滤掉价格或使用量小于等于 0 的异常数据
    if all(col in df.columns for col in target_cols):
        df = df[(df["Gas Price"] > 0) & (df["Gas Used"] > 0)]

    # 5. 保存结果
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"数据清洗完成！清洗后剩余 {len(df)} 行，已保存至: {output_path}")


if __name__ == "__main__":
    INPUT_FILE = os.path.join("data", "raw", "raw_data.xlsx")
    OUTPUT_FILE = os.path.join("data", "cleaned", "clean_data.xlsx")
    clean_dataset(INPUT_FILE, OUTPUT_FILE)
