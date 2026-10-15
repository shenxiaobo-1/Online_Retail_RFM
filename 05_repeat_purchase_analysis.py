
from pathlib import Path
import pandas as pd

# 1. 读取清洗后的数据
project_dir = Path(__file__).resolve().parent
file_path = project_dir / "output" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path)

# 2. 统计每位客户购买过的不同订单数
customer_orders = (
    df.groupby("CustomerID")["InvoiceNo"]
    .nunique()
    .reset_index(name="OrderCount")
)

# 3. 计算客户整体复购情况
total_customers = customer_orders["CustomerID"].nunique()

repeat_customers = (
    customer_orders["OrderCount"] >= 2
).sum()

one_time_customers = (
    customer_orders["OrderCount"] == 1
).sum()

repeat_rate = repeat_customers / total_customers * 100

average_orders = customer_orders["OrderCount"].mean()

# 4. 输出核心指标
print("========== 用户复购分析 ==========")
print("客户总数：", total_customers)
print("复购客户数：", repeat_customers)
print("一次性购买客户数：", one_time_customers)
print("复购客户占比：", round(repeat_rate, 2), "%")
print("每位客户平均订单数：", round(average_orders, 2))

# 5. 查看购买订单数最多的前10位客户
top_customers = customer_orders.sort_values(
    "OrderCount", ascending=False
).head(10)

print("\n========== 订单数最多的前10位客户 ==========")
print(top_customers.to_string(index=False))

# 6. 保存客户订单次数明细
output_path = project_dir / "output" / "customer_order_counts.csv"
customer_orders.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\n客户订单次数明细已保存：", output_path)
