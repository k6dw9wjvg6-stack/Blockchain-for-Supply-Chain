import os
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
def draw_group_cost_comparison(output_img: str) -> None:
    """绘制A组与B组平均响应成本RC的对比柱状图。"""
    groups = ["A组\n（普通转账）", "B组\n（智能合约调用）"]
    cost = [65857.19, 111293.44]
    plt.figure(figsize=(6, 5))
    plt.bar(groups, cost, color=["royalblue", "red"], width=0.5) 
    plt.ylabel("平均响应成本 RC")
    plt.title("图4-3 A/B组平均响应成本对比图")
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    # 自动创建输出目录并保存
    os.makedirs(os.path.dirname(output_img), exist_ok=True)
    plt.savefig(output_img, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 图4-3 已成功保存至: {output_img}")
if __name__ == "__main__":
    OUTPUT_IMAGE = os.path.join("output", "images", "图4-3_A_B组平均响应成本对比图.png")
    draw_group_cost_comparison(OUTPUT_IMAGE)
