
from pathlib import Path
import pandas as pd

# 1. 读取 RFM 明细
project_dir = Path(__file__).resolve().parent
input_path = project_dir / "output" / "customer_rfm.csv"
output_dir = project_dir / "output"

rfm = pd.read_csv(input_path)

# 2. 为 R、F、M 分别打 1—5 分
# R 越小越好，因此反向评分
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# F、M 越大越好，因此正向评分
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# 3. 计算 RFM 总分
rfm["RFM_TotalScore"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

# 4. 组合三个维度的得分
rfm["RFM_SegmentCode"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

# 5. 输出打分结果
print("========== RFM 打分结果 ==========")
print("客户总数：", len(rfm))

print("\n========== 各项得分分布 ==========")
for col in ["R_Score", "F_Score", "M_Score"]:
    print(f"\n{col}：")
    print(rfm[col].value_counts().sort_index())

print("\n========== RFM 得分前10位客户 ==========")
top_customers = rfm.sort_values(
    "RFM_TotalScore", ascending=False
).head(10)

print(
    top_customers[
        ["CustomerID", "Recency", "Frequency", "Monetary",
         "R_Score", "F_Score", "M_Score",
         "RFM_TotalScore", "RFM_SegmentCode"]
    ].to_string(index=False)
)

# 6. 保存打分结果
output_path = output_dir / "customer_rfm_scored.csv"
rfm.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nRFM 打分结果已保存：", output_path)
