import os
import pandas as pd

# 常量定义（大写）
RT_CONSTANT = 1


def calculate_metrics(input_path: str, output_path: str) -> None:
    """基于清洗后的数据计算总成本(RC)与燃气效率(RE)指标。"""
    if not os.path.exists(input_path):
        print(f"Error: 找不到清洗后的数据文件 {input_path}，请先运行 clean_data.py")
        return

    df = pd.read_excel(input_path)

    print("正在计算 RC 和 RE 指标...")
    # 计算总成本 RC = Gas Price * Gas Used
    df["RC"] = df["Gas Price"] * df["Gas Used"]

    # 计算 RE = 1 / (RT * RC)
    # 注意：如果 RC 为 0 可能会触发除以零报错，前面清洗已过滤掉 <=0 的值，此处相对安全
    df["RE"] = 1 / (RT_CONSTANT * df["RC"])

    # 自动创建输出目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_excel(output_path, index=False)
    print(f"指标计算完成！结果已成功保存至: {output_path}")


if __name__ == "__main__":
    INPUT_FILE = os.path.join("data", "cleaned", "clean_data.xlsx")
    OUTPUT_FILE = os.path.join("output", "tables", "result.xlsx")
    calculate_metrics(INPUT_FILE, OUTPUT_FILE)
