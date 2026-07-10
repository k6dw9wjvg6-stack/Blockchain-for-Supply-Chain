import os
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
def plot_gas_price_boxplot(result_file: str, output_img: str) -> None:
    """从生成的结果文件中读取 Gas Price 数据并绘制箱线图。"""
    if not os.path.exists(result_file):
        print(f"❌ 错误: 找不到结果文件 {result_file}，请确保前置计算已完成。")
        return
    df = pd.read_excel(result_file)
