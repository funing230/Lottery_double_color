import pandas as pd


def remove_irrelevant_features(df):
    """
    根据字段名称删除对建模没有意义的特征，并从 detailsLink 字段中提取编号。
    要删除的特征包括：常量/描述性文本字段、低完整性字段、URL字段等。
    同时，将 detailsLink 中包含的数字提取出来，保存在新列 "detailsNum" 中。
    """
    # 提取 detailsLink 中的数字，提取模式：最后一个斜杠后面到 .shtml 之间的数字
    if "detailsLink" in df.columns:
        df["detailsNum"] = df["detailsLink"].str.extract(r'/(\d+)\.shtml')[0]

    # 要删除的字段列表（根据你的分析结果调整）
    cols_to_drop = [
        "name",  # 常量，始终为“双色球”
        "videoLink",  # URL字段
        "blue2",  # 缺失率极高
        "content",  # 描述性文本
        "addmoney",  # 缺失率高
        "addmoney2",  # 缺失率高
        "msg",  # 缺失率高
        "z2add",  # 缺失率高
        "m2add",  # 缺失率高
        "detailsLink",  # URL字段
        "date",  # 与“开奖日期”重复
        "mj1",  # 低完整性或意义不明确
        "mj6",  # 低完整性或意义不明确
        "zj1",  # 低完整性或意义不明确
        "zj6",  # 低完整性或意义不明确
    ]

    # 地域分布的字段（这些数据对预测通常意义不大）
    region_columns = [
        "上海", "云南", "内蒙古", "北京", "吉林", "四川", "天津", "宁夏",
        "安徽", "山东", "山西", "广东", "广西", "新疆", "江苏", "江西",
        "河北", "河南", "浙江", "海南", "深圳", "湖北", "湖南", "甘肃",
        "福建", "西藏", "贵州", "辽宁", "重庆", "陕西", "青海", "黑龙江"
    ]
    cols_to_drop.extend(region_columns)

    # 过滤掉不存在的列
    cols_to_drop = [col for col in cols_to_drop if col in df.columns]

    # 删除这些指定的列
    df_clean = df.drop(columns=cols_to_drop)
    return df_clean


def main():
    # 加载已存在的合并文件 merged_output.csv
    df = pd.read_csv("0.8merged_output.csv", encoding="utf-8")
    print("原始文件中总列数:", df.shape[1])
    print("原始列名称：", df.columns.tolist())

    # 删除不需要的特征，并提取 detailsLink 中的数字
    df_clean = remove_irrelevant_features(df)
    print("\n删除无意义特征后，总列数:", df_clean.shape[1])
    print("剩余列名称：", df_clean.columns.tolist())

    # 保存清洗后的数据到新的 CSV 文件中
    df_clean.to_csv("1.merged_output_cleaned.csv", index=False, encoding="utf-8")
    print("已保存清洗后的文件 1.merged_output_cleaned.csv")


if __name__ == "__main__":
    main()
