
from pathlib import Path
import pandas as pd

# 1. 读取原始数据
project_dir = Path(__file__).resolve().parent
file_path = project_dir / "data" / "Online Retail.xlsx"

df = pd.read_excel(file_path, engine="openpyxl")

# 2. 统计取消订单
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

print("========== 订单检查 ==========")
print("总记录数：", len(df))
print("取消订单记录数：", cancelled.sum())
print("非取消订单记录数：", (~cancelled).sum())

# 3. 检查购买数量
print("\n========== Quantity 检查 ==========")
print("数量小于或等于0的记录数：", (df["Quantity"] <= 0).sum())
print("数量大于0的记录数：", (df["Quantity"] > 0).sum())
print("数量最小值：", df["Quantity"].min())
print("数量最大值：", df["Quantity"].max())

# 4. 检查商品单价
print("\n========== UnitPrice 检查 ==========")
print("单价小于或等于0的记录数：", (df["UnitPrice"] <= 0).sum())
print("单价大于0的记录数：", (df["UnitPrice"] > 0).sum())
print("单价最小值：", df["UnitPrice"].min())
print("单价最大值：", df["UnitPrice"].max())

# 5. 检查客户编号缺失情况
print("\n========== CustomerID 检查 ==========")
print("客户编号缺失记录数：", df["CustomerID"].isna().sum())
print("客户编号非缺失记录数：", df["CustomerID"].notna().sum())
print("有效客户编号去重数量：", df["CustomerID"].nunique())

# 6. 检查完成
print("\n数据质量检查完成！")


print("\n========== 待确认的清洗信息 ==========")

cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

print("取消订单记录数：", cancelled.sum())
print("Quantity <= 0：", (df["Quantity"] <= 0).sum())
print("Quantity 最小值：", df["Quantity"].min())
print("Quantity 最大值：", df["Quantity"].max())
print("UnitPrice <= 0：", (df["UnitPrice"] <= 0).sum())
print("UnitPrice 最小值：", df["UnitPrice"].min())
print("UnitPrice 最大值：", df["UnitPrice"].max())
