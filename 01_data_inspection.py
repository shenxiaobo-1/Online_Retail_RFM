
from pathlib import Path
import pandas as pd

# 第1步：找到 Excel 数据文件
project_dir = Path(__file__).resolve().parent
file_path = project_dir / "data" / "Online Retail.xlsx"

# 第2步：检查文件是否存在
print("正在检查数据文件……")

if not file_path.exists():
    raise FileNotFoundError(
        f"找不到文件：{file_path}\n"
        "请检查 data 文件夹和 Excel 文件名。"
    )

print("数据文件已找到！")

# 第3步：读取 Excel 数据
print("正在读取 Excel 数据，请稍等……")
df = pd.read_excel(file_path, engine="openpyxl")

# 第4步：查看数据规模
print("\n========== 数据规模 ==========")
print("总行数：", df.shape[0])
print("总列数：", df.shape[1])

# 第5步：查看前5行
print("\n========== 前5行数据 ==========")
print(df.head().to_string())

# 第6步：查看字段名称
print("\n========== 字段名称 ==========")
print(df.columns.tolist())

# 第7步：查看字段类型
print("\n========== 字段类型 ==========")
print(df.dtypes)

# 第8步：统计每列缺失值
print("\n========== 缺失值统计 ==========")
print(df.isnull().sum())

print("\n数据检查完成！")

