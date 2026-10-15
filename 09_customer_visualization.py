
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 路径设置
project_dir = Path(__file__).resolve().parent
output_dir = project_dir / "output"

summary_path = output_dir / "customer_segment_summary.csv"
rfm_path = output_dir / "customer_rfm_segmented.csv"

summary = pd.read_csv(summary_path)
rfm = pd.read_csv(rfm_path)

# 中文显示设置（Windows 常见字体）
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei", "SimHei", "Arial"
]
plt.rcParams["axes.unicode_minus"] = False

# 图表输出目录
chart_dir = output_dir / "charts"
chart_dir.mkdir(exist_ok=True)

# 统一按照客户数量排序
summary_count = summary.sort_values(
    "CustomerCount", ascending=True
)

# 图1：客户分层人数
plt.figure(figsize=(10, 6))
plt.barh(
    summary_count["CustomerSegment"],
    summary_count["CustomerCount"]
)
plt.title("Customer Segment Distribution")
plt.xlabel("Number of Customers")
plt.ylabel("Customer Segment")
plt.tight_layout()
plt.savefig(
    chart_dir / "01_customer_segment_count.png",
    dpi=300, bbox_inches="tight"
)
plt.close()

# 图2：各客户群体销售额贡献
summary_sales = summary.sort_values(
    "TotalMonetary", ascending=True
)

plt.figure(figsize=(10, 6))
plt.barh(
    summary_sales["CustomerSegment"],
    summary_sales["TotalMonetary"]
)
plt.title("Sales Contribution by Customer Segment")
plt.xlabel("Total Sales")
plt.ylabel("Customer Segment")
plt.tight_layout()
plt.savefig(
    chart_dir / "02_customer_segment_sales.png",
    dpi=300, bbox_inches="tight"
)
plt.close()

# 图3：各群体平均购买频率与平均消费金额
plt.figure(figsize=(10, 6))
plt.scatter(
    summary["AvgFrequency"],
    summary["AvgMonetary"],
    s=summary["CustomerCount"] * 2,
    alpha=0.7
)

for _, row in summary.iterrows():
    plt.annotate(
        row["CustomerSegment"],
        (row["AvgFrequency"], row["AvgMonetary"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

plt.title("Customer Segment: Frequency vs Monetary")
plt.xlabel("Average Number of Orders")
plt.ylabel("Average Customer Spending")
plt.tight_layout()
plt.savefig(
    chart_dir / "03_frequency_vs_monetary.png",
    dpi=300, bbox_inches="tight"
)
plt.close()

print("三张图表已生成：")
for file in sorted(chart_dir.glob("*.png")):
    print(file)
