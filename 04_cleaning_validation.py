
from pathlib import Path
import pandas as pd

# 1. 读取清洗后的数据
project_dir = Path(__file__).resolve().parent
file_path = project_dir / "output" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path)

# 2. 检查基本情况
print("========== 清洗结果核验 ==========")
print("记录数：", len(df))
print("客户数：", df["CustomerID"].nunique())
print("订单数：", df["InvoiceNo"].nunique())

# 3. 检查是否还有无效记录
print("\n========== 数据质量检查 ==========")
print("客户编号缺失数：", df["CustomerID"].isna().sum())
print("取消订单数：", df["InvoiceNo"].astype(str).str.startswith("C").sum())
print("Quantity <= 0：", (df["Quantity"] <= 0).sum())
print("UnitPrice <= 0：", (df["UnitPrice"] <= 0).sum())

# 4. 核对金额计算
expected_amount = (df["Quantity"] * df["UnitPrice"]).sum()
actual_amount = df["TotalAmount"].sum()

print("\n========== 金额核验 ==========")
print("重新计算金额：", round(expected_amount, 2))
print("保存的金额合计：", round(actual_amount, 2))
print("金额是否一致：", abs(expected_amount - actual_amount) < 0.01)

# 5. 检查日期范围
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("\n========== 日期范围 ==========")
print("最早交易时间：", df["InvoiceDate"].min())
print("最晚交易时间：", df["InvoiceDate"].max())

print("\n核验完成！")
