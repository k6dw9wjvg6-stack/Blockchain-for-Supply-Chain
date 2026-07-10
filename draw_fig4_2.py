import os
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
def draw_metrics_comparison(output_img: str) -> None:
    """绘制高低Gas环境多指标对比条形图。"""
    labels = ["平均Gas Price\n(Gwei)", "平均Gas Used", "平均响应成本 RC"]
    low = [0.929, 133240.52, 88575.92]
    high = [1.985, 77564.67, 141008.21]
    x = np.arange(len(labels))
    width = 0.35
    plt.figure(figsize=(7, 5))
    plt.bar(x - width / 2, low, width, color="royalblue", label="低Gas环境（n=5892）")
    plt.bar(x + width / 2, high, width, color="red", label="高Gas环境（n=5900）")
    plt.xticks(x, labels)
    plt.ylabel("数值")
    plt.title("图4-2 高低Gas环境指标对比图")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    # 自动创建输出目录并保存
    os.makedirs(os.path.dirname(output_img), exist_ok=True)
    plt.savefig(output_img, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 图4-2 已成功保存至: {output_img}")
if __name__ == "__main__":
    OUTPUT_IMAGE = os.path.join("output", "images", "图4-2_高低Gas环境指标对比图.png")
    draw_metrics_comparison(OUTPUT_IMAGE)
