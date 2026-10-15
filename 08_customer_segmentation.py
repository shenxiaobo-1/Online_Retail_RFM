
from pathlib import Path
import pandas as pd

# 1. 设置项目路径
project_dir = Path(__file__).resolve().parent
input_path = project_dir / "output" / "customer_rfm_scored.csv"
output_dir = project_dir / "output"

# 2. 读取已经完成评分的客户数据
rfm = pd.read_csv(input_path)

# 3. 根据 RFM 评分划分客户群体
def classify_customer(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 4:
        return "Loyal Customers"
    elif r <= 2 and m >= 4:
        return "High Value At Risk"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r >= 4 and f >= 2:
        return "Potential Loyalists"
    elif r >= 4 and f == 1:
        return "Recent Customers"
    elif r <= 2 and f <= 2:
        return "Hibernating"
    else:
        return "Need Attention"


rfm["CustomerSegment"] = rfm.apply(classify_customer, axis=1)

# 4. 保存每位客户的分层结果
customer_output = output_dir / "customer_rfm_segmented.csv"
rfm.to_csv(customer_output, index=False, encoding="utf-8-sig")

# 5. 统计各类客户的数量和消费情况
summary = (
    rfm.groupby("CustomerSegment")
    .agg(
        CustomerCount=("CustomerID", "count"),
        AvgRecency=("Recency", "mean"),
        AvgFrequency=("Frequency", "mean"),
        AvgMonetary=("Monetary", "mean"),
        MedianMonetary=("Monetary", "median"),
        TotalMonetary=("Monetary", "sum")
    )
    .reset_index()
)

summary["CustomerSharePct"] = (
    summary["CustomerCount"] / len(rfm) * 100
).round(2)

summary = summary.sort_values(
    "CustomerCount", ascending=False
)

summary_output = output_dir / "customer_segment_summary.csv"
summary.to_csv(summary_output, index=False, encoding="utf-8-sig")

# 6. 打印结果
print("========== 客户分层数量 ==========")
print(summary[
    ["CustomerSegment", "CustomerCount", "CustomerSharePct"]
].to_string(index=False))

print("\n========== 各类客户消费情况 ==========")
print(summary.round(2).to_string(index=False))

print("\n客户总数：", len(rfm))
print("分层客户数量合计：", summary["CustomerCount"].sum())
print("客户明细已保存：", customer_output)
print("分层汇总已保存：", summary_output)
