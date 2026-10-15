
from pathlib import Path
import pandas as pd

# 1. 定位原始数据与输出目录
project_dir = Path(__file__).resolve().parent
input_path = project_dir / "data" / "Online Retail.xlsx"
output_dir = project_dir / "output"

# 如果 output 文件夹不存在，就自动创建
output_dir.mkdir(parents=True, exist_ok=True)

# 2. 读取原始数据
df = pd.read_excel(input_path, engine="openpyxl")

print("原始记录数：", len(df))

# 3. 统计原始数据中的关键问题
missing_customer = df["CustomerID"].isna().sum()
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

print("客户编号缺失记录数：", missing_customer)
print("取消订单记录数：", cancelled.sum())

# 4. 去除无法识别客户的记录
clean_df = df[df["CustomerID"].notna()].copy()

# 5. 排除取消订单
clean_df = clean_df[
    ~clean_df["InvoiceNo"].astype(str).str.startswith("C")
].copy()

# 6. 仅保留正向购买记录
clean_df = clean_df[
    (clean_df["Quantity"] > 0)
    & (clean_df["UnitPrice"] > 0)
].copy()

# 7. 计算每条商品明细的金额
clean_df["TotalAmount"] = (
    clean_df["Quantity"] * clean_df["UnitPrice"]
)

# 8. 统一客户编号格式
clean_df["CustomerID"] = (
    clean_df["CustomerID"].astype("int64").astype(str)
)

# 9. 输出清洗结果
output_path = output_dir / "online_retail_cleaned.csv"
clean_df.to_csv(output_path, index=False, encoding="utf-8-sig")

# 10. 展示清洗前后的数据规模
print("\n========== 清洗结果 ==========")
print("原始记录数：", len(df))
print("清洗后记录数：", len(clean_df))
print("排除记录数：", len(df) - len(clean_df))
print("清洗后客户数：", clean_df["CustomerID"].nunique())
print("清洗后订单数：", clean_df["InvoiceNo"].nunique())
print("清洗后销售金额：", round(clean_df["TotalAmount"].sum(), 2))
print("输出文件：", output_path)

print("\n清洗完成！")
