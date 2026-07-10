import os
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
def draw_re_efficiency_trend(output_img: str) -> None:
    """绘制高低Gas环境下RE响应效率的变化折线图。"""
    x = ["低Gas环境\n(n=5892)", "高Gas环境\n(n=5900)"]
    re = [4.80e-5, 1.56e-5]
    plt.figure(figsize=(6, 5))
    plt.plot(x, re, color="royalblue", marker="o", linewidth=2)
    plt.ylabel("平均RE（1/(RT×RC)）")
    plt.title("图4-4 RE响应效率变化图")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    # 自动创建输出目录并保存
    os.makedirs(os.path.dirname(output_img), exist_ok=True)
    plt.savefig(output_img, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 图4-4 已成功保存至: {output_img}")
if __name__ == "__main__":
    OUTPUT_IMAGE = os.path.join("output", "images", "图4-4_RE响应效率变化图.png")
    draw_re_efficiency_trend(OUTPUT_IMAGE)
