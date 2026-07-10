import os
import numpy as np
import pandas as pd
def stratified_sample(group_df: pd.DataFrame, target_size: int) -> pd.DataFrame:
    """按小时时间段比例对数据组进行精细分层抽样。"""
    group_name = str(group_df["group_type"].iloc[0])
    print(f"\n开始处理分层抽样：{group_name}")
    current_size = len(group_df)
    if current_size < target_size:
        raise ValueError(f"❌ {group_name} 数据量不足。当前: {current_size}, 目标: {target_size}")
    # 计算时间按小时分布比例
    hour_counts = group_df["hour_segment"].value_counts().sort_index()
    proportions = hour_counts / hour_counts.sum()
    # 初始计算分配的基数
    sample_counts = np.floor(proportions * target_size).astype(int)
    remain = target_size - sample_counts.sum()
    # 解决余数分配，确保总数完全等于 target_size
    if remain > 0:
        decimal_part = (proportions * target_size) - sample_counts
        add_hours = decimal_part.sort_values(ascending=False).index[:remain]
        for h in add_hours:
            sample_counts[h] += 1
    sampled_parts = []
    for hour, sample_num in sample_counts.items():
        subset = group_df[group_df["hour_segment"] == hour]
        sampled = subset.sample(n=min(sample_num, len(subset)), replace=False, random_state=42)
        sampled_parts.append(sampled)
    result = pd.concat(sampled_parts, ignore_index=False)
    # 兜底：防止小概率截断导致的少抽
    if len(result) < target_size:
        need = target_size - len(result)
        remain_df = group_df.loc[~group_df.index.isin(result.index)]
        extra = remain_df.sample(n=need, replace=False, random_state=42)
        result = pd.concat([result, extra])
    # 打乱样本顺序
    return result.sample(frac=1, random_state=42)
def process_high_congestion(file_path: str, target_num: int = 2950) -> None:
    """读取、校验、按组分层抽样并合并高拥堵数据。"""
    if not os.path.exists(file_path):
        print(f"❌ 错误: 找不到高拥堵原始文件 {file_path}")
        return
    print(f"正在读取文件：{file_path}")
    df = pd.read_excel(file_path, engine="openpyxl")
    print(f"原始总记录数：{len(df)}")
    # 检查核心字段
    required_cols = ["group_type", "block_time"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"缺少必要字段：{col}。当前包含的字段有：{list(df.columns)}")
    # 时间解析与分段
    df["block_time"] = pd.to_datetime(df["block_time"])
    df["hour_segment"] = df["block_time"].dt.hour
    # 分组切片
    group_a = df[df["group_type"].astype(str).str.contains("A组", na=False)]
    group_b = df[df["group_type"].astype(str).str.contains("B组", na=False)]
    print(f"\n[数据统计] A组可用数量: {len(group_a)} | B组可用数量: {len(group_b)}")
    if len(group_a) == 0 or len(group_b) == 0:
        raise ValueError("❌ 未能成功筛选出完整的 A组 或 B组 数据，请核对表格中的 group_type 列值！")
    # 执行分层抽样
    sampled_a = stratified_sample(group_a, target_num)
    sampled_b = stratified_sample(group_b, target_num)
    # 合并、清洗中间列
    result = pd.concat([sampled_a, sampled_b], ignore_index=True)
    result = result.drop(columns=["hour_segment"])
    # 动态计算输出路径
    base_dir = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(base_dir, f"{file_name}_AB各{target_num}条_保持时段比例.xlsx")
    result.to_excel(output_path, index=False, engine="openpyxl")
    print(f"\n处理成功！\n💾 最终合并数据已导出至：{output_path}\n📊 最终总量：{len(result)}")
    print(result["group_type"].value_counts())
if __name__ == "__main__":
    # 修改为项目通用的相对路径
    HIGH_CONGESTION_DATA = os.path.join("data", "raw", "高拥堵数据.xlsx")
    process_high_congestion(HIGH_CONGESTION_DATA)
