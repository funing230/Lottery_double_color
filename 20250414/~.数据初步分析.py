import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 配置 matplotlib 支持中文显示以及负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定支持中文的字体，例如黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

def load_data(csv_file='0.8merged_output.csv'):
    """
    读取 merged_output.csv 文件，确保所有数据都被正确载入。
    """
    df = pd.read_csv(csv_file, encoding='utf-8')
    return df

def check_duplicates(df):
    """
    检查数据中的重复行，并输出重复行数和重复率信息。
    """
    total_rows = df.shape[0]
    duplicate_rows = df.duplicated().sum()
    duplicate_rate = duplicate_rows / total_rows * 100
    print("\n========== 重复率检查 ==========")
    print(f"重复行数量：{duplicate_rows}（占总数据的 {duplicate_rate:.2f}%）")
    if duplicate_rows > 0:
        print("重复行示例：")
        print(df[df.duplicated()].head())

def basic_info(df):
    print("\n========== 数据基本信息 ==========")
    print("数据总行数：", df.shape[0])
    print("数据总列数：", df.shape[1])
    print("\n各列数据类型及非空情况：")
    df.info()
    print("\n========== 数值统计描述（describe） ==========")
    # 将可能为数字的列转换为数值（转换错误的会变为 NaN）
    numeric_cols = ['sales', 'poolmoney',
                    '一等奖注数', '一等奖金额',
                    '二等奖注数', '二等奖金额',
                    '三等奖注数', '三等奖金额',
                    '奖项4注数', '奖项4金额',
                    '奖项5注数', '奖项5金额',
                    '奖项6注数', '奖项6金额',
                    '奖项7注数', '奖项7金额']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    print(df[numeric_cols].describe())

def missing_value_analysis(df):
    print("\n========== 缺失值统计 ==========")
    missing_counts = df.isnull().sum()
    total_rows = df.shape[0]
    for col in df.columns:
        non_null = df[col].count()
        missing = missing_counts[col]
        percent = non_null / total_rows * 100
        print(f"{col}: 有效值 {non_null} / {total_rows} ({percent:.2f}%)，缺失 {missing} 个")

def advanced_info(df):
    total_rows, total_cols = df.shape
    print("\n========== 高级数据信息 ==========")
    print(f"数据总量：{total_rows} 条记录，{total_cols} 列")
    print("每一列的完整性信息如下：")
    info_df = pd.DataFrame({
        "非空值数量": df.count(),
        "缺失值数量": df.isnull().sum(),
    })
    info_df["完整性(%)"] = info_df["非空值数量"] / total_rows * 100
    print(info_df)

def categorical_analysis(df):
    print("\n========== 分类变量频数统计 ==========")
    if 'name' in df.columns:
        print("彩票名称频次：")
        print(df['name'].value_counts())
    if 'week' in df.columns:
        print("\n开奖星期频次：")
        print(df['week'].value_counts())

def plot_distribution(df):
    # 绘制主要数值变量的直方图
    numeric_cols = ['sales', 'poolmoney',
                    '一等奖注数', '一等奖金额',
                    '二等奖注数', '二等奖金额',
                    '三等奖注数', '三等奖金额',
                    '奖项4注数', '奖项4金额',
                    '奖项5注数', '奖项5金额',
                    '奖项6注数', '奖项6金额',
                    '奖项7注数', '奖项7金额']
    for col in numeric_cols:
        if col in df.columns:
            plt.figure(figsize=(6, 4))
            df[col].hist(bins=20, edgecolor='k')
            plt.title(f"{col} 分布")
            plt.xlabel(col)
            plt.ylabel("频数")
            plt.tight_layout()
            plt.show()

def correlation_analysis(df):
    # 计算主要数值变量的相关性矩阵
    numeric_cols = ['sales', 'poolmoney',
                    '一等奖注数', '一等奖金额',
                    '二等奖注数', '二等奖金额',
                    '三等奖注数', '三等奖金额',
                    '奖项4注数', '奖项4金额',
                    '奖项5注数', '奖项5金额',
                    '奖项6注数', '奖项6金额',
                    '奖项7注数', '奖项7金额']
    corr_matrix = df[numeric_cols].corr()
    print("\n========== 相关性矩阵 ==========")
    print(corr_matrix)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("主要数值变量相关性热力图")
    plt.tight_layout()
    plt.show()

def red_ball_analysis(df):
    print("\n========== 红球号码频次统计 ==========")
    if 'red' not in df.columns:
        print("无 red 列数据！")
        return
    # 拆分 red 字段中的号码（假设以空格分隔，例如 "02 06 08 09 10 24"）
    red_numbers = df['red'].dropna().apply(lambda x: x.split())
    red_numbers_flat = [num for sublist in red_numbers for num in sublist]
    red_series = pd.Series(red_numbers_flat)
    red_freq = red_series.value_counts().sort_index()
    print(red_freq)
    plt.figure(figsize=(8, 4))
    red_freq.plot(kind='bar', edgecolor='k')
    plt.title("红球号码出现频次")
    plt.xlabel("红球号码")
    plt.ylabel("频次")
    plt.tight_layout()
    plt.show()

def boxplot_analysis(df):
    # 绘制箱线图检测销售额和奖池金额的异常值情况
    numeric_cols = ['sales', 'poolmoney']
    for col in numeric_cols:
        if col in df.columns:
            plt.figure(figsize=(6, 4))
            sns.boxplot(y=df[col])
            plt.title(f"{col} 箱线图")
            plt.tight_layout()
            plt.show()

def main():
    # 加载已存在的合并文件
    df = load_data("merged_output.csv")

    # 重复数据检查
    check_duplicates(df)

    # 打印基本信息与高级信息
    basic_info(df)
    missing_value_analysis(df)
    advanced_info(df)

    # 分类变量频数统计
    categorical_analysis(df)

    # 绘制直方图和箱线图
    plot_distribution(df)
    boxplot_analysis(df)

    # 相关性分析
    correlation_analysis(df)

    # 红球号码频次统计
    red_ball_analysis(df)

if __name__ == "__main__":
    main()
