import pandas as pd

# 读取两个 CSV 文件，注意编码方式根据实际情况调整（例如 utf-8）
df1 = pd.read_csv("ssq_winning_records_all.csv", encoding="utf-8")
df2 = pd.read_csv("0.5ssq_details_extracted.csv", encoding="utf-8")

# 使用 outer join 按照 "code" 字段合并两个 DataFrame
merged_df = pd.merge(df1, df2, on="code", how="outer", suffixes=("_1", "_2"))

# 对于重复的字段（即同时出现在 df1 与 df2 中的字段，排除 "code"），
# 使用 combine_first() 方法合并（即对于该字段，取 _1 中非空值，否则使用 _2）
common_columns = set(df1.columns).intersection(df2.columns)
common_columns.discard("code")  # 排除 code 字段

for col in common_columns:
    # 生成合并后的新列，先尝试 df1 中的值，如果为 NaN 则使用 df2 中的值
    merged_df[col] = merged_df[f"{col}_1"].combine_first(merged_df[f"{col}_2"])
    # 删除原来的重复列
    merged_df.drop([f"{col}_1", f"{col}_2"], axis=1, inplace=True)

# 其余不重复的字段已经自动合并，更新后的 DataFrame 中列名就是并集

# 保存合并后的结果到一个新的 CSV 文件中
merged_df.to_csv("0.8merged_output.csv", index=False, encoding="utf-8")
print("合并完成，结果保存在 merged_output.csv 中")
