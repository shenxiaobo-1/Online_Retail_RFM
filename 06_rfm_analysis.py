
from pathlib import Path
import pandas as pd

# 1. 读取清洗后的数据
project_dir = Path(__file__).resolve().parent
input_path = project_dir / "output" / "online_retail_cleaned.csv"
output_dir = project_dir / "output"

df = pd.read_csv(input_path)

# 2. 将订单日期转换成日期时间格式
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 3. 设置分析基准日
analysis_date = pd.Timestamp("2011-12-10")

# 4. 按客户计算 R、F、M
rfm = df.groupby("CustomerID").agg(
    LastPurchaseDate=("InvoiceDate", "max"),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalAmount", "sum")
).reset_index()

# 5. 计算 Recency：距分析基准日的天数
rfm["Recency"] = (
    analysis_date - rfm["LastPurchaseDate"].dt.normalize()
).dt.days

# 6. 调整字段顺序
rfm = rfm[
    ["CustomerID", "LastPurchaseDate", "Recency",
     "Frequency", "Monetary"]
]

# 7. 输出基本统计结果
print("========== RFM 基本统计 ==========")
print("客户数：", len(rfm))
print("\n========== RFM 描述统计 ==========")
print(rfm[["Recency", "Frequency", "Monetary"]].describe().round(2))

print("\n========== RFM 前5行 ==========")
print(rfm.head().to_string(index=False))

# 8. 保存 RFM 明细
output_path = output_dir / "customer_rfm.csv"
rfm.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nRFM 明细已保存：", output_path)
