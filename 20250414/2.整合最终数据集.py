import pandas as pd

# 读取文件（请根据实际文件路径调整文件名及编码）
df1 = pd.read_csv("1.5merged_output_final_cleaned.csv", encoding="utf-8")
df2 = pd.read_csv("1.8processed_first_winning_regions_by_province.csv", encoding="utf-8")

# 检查各数据集的列名
print("df1 columns:", df1.columns.tolist())
print("df2 columns:", df2.columns.tolist())

# 对于 df1，如果存在 'Code' 列则转换；如果没有，则尝试 'code'
if 'Code' in df1.columns:
    df1["code_lower"] = df1["Code"].astype(str).str.lower()
elif 'code' in df1.columns:
    df1["code_lower"] = df1["code"].astype(str).str.lower()
else:
    raise KeyError("df1中未找到 'Code' 或 'code' 列。")

# 对于 df2，类似处理
if 'Code' in df2.columns:
    df2["code_lower"] = df2["Code"].astype(str).str.lower()
elif 'code' in df2.columns:
    df2["code_lower"] = df2["code"].astype(str).str.lower()
else:
    raise KeyError("df2中未找到 'Code' 或 'code' 列。")

# 合并时以辅助列 "code_lower" 为键进行内连接
merged_df = pd.merge(df1, df2, on="code_lower", how="inner")

# 删除不需要的辅助列和 "FirstWinningRegions"、"FirstWinningRegions.1" 列
columns_to_drop = ["code_lower"]
if "FirstWinningRegions" in merged_df.columns:
    columns_to_drop.append("FirstWinningRegions")
if "FirstWinningRegions.1" in merged_df.columns:
    columns_to_drop.append("FirstWinningRegions.1")
merged_df.drop(columns=columns_to_drop, inplace=True)

# 确保 FirstPrizeAmount 列为字符串类型后，使用正则表达式替换掉括号及其中内容
# 将 FirstPrizeAmount 列转换为字符串后，用正则表达式替换中文括号及其中内容，再去除首尾空白
merged_df["FirstPrizeAmount"] = merged_df["FirstPrizeAmount"].astype(str).str.replace(r'（.*?）', '', regex=True).str.strip()


# 保存合并后的数据集
merged_df.to_csv("2.merged_dataset.csv", index=False, encoding="utf-8")
print("合并后的数据已保存到 2.merged_dataset.csv")
