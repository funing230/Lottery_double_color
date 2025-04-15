import pandas as pd
import re
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 配置 matplotlib 支持中文显示以及负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


##############################################
# 第一步：二次清洗与转换函数
##############################################
def load_data(csv_file="merged_output_cleaned.csv"):
    """读取 CSV 文件"""
    df = pd.read_csv(csv_file, encoding="utf-8")
    return df


def drop_winning_numbers(df):
    """删除‘WinningNumbers’（或‘开奖号码’）列"""
    if "WinningNumbers" in df.columns:
        return df.drop(columns=["WinningNumbers"])
    elif "开奖号码" in df.columns:
        return df.drop(columns=["开奖号码"])
    else:
        return df


def rename_columns(df):
    """将中文列名转换为英文列名"""
    mapping = {
        "code": "Code",
        "week": "Week",
        "red": "RedNumbers",
        "blue": "BlueBall",
        "sales": "Sales",
        "poolmoney": "PoolMoney",
        "一等奖注数": "FirstPrizeCount",
        "一等奖金额": "FirstPrizeAmount",
        "二等奖注数": "SecondPrizeCount",
        "二等奖金额": "SecondPrizeAmount",
        "三等奖注数": "ThirdPrizeCount",
        "三等奖金额": "ThirdPrizeAmount",
        "奖项4注数": "FourthPrizeCount",
        "奖项4金额": "FourthPrizeAmount",
        "奖项5注数": "FifthPrizeCount",
        "奖项5金额": "FifthPrizeAmount",
        "奖项6注数": "SixthPrizeCount",
        "奖项6金额": "SixthPrizeAmount",
        "奖项7注数": "SeventhPrizeCount",
        "奖项7金额": "SeventhPrizeAmount",
        "开奖日期": "DrawDate",
        "本期销售金额": "CurrentSales",
        # "开奖号码" 列删除
        "一等奖中奖注数": "FirstWinningCount",
        "一等奖单注中奖金额": "FirstWinningAmount",
        "二等奖中奖注数": "SecondWinningCount",
        "二等奖单注中奖金额": "SecondWinningAmount",
        "三等奖中奖注数": "ThirdWinningCount",
        "三等奖单注中奖金额": "ThirdWinningAmount",
        "四等奖中奖注数": "FourthWinningCount",
        "四等奖单注中奖金额": "FourthWinningAmount",
        "五等奖中奖注数": "FifthWinningCount",
        "五等奖单注中奖金额": "FifthWinningAmount",
        "六等奖中奖注数": "SixthWinningCount",
        "六等奖单注中奖金额": "SixthWinningAmount",
        "一等奖中奖情况": "FirstWinningRegions",
        "下期一等奖奖池累计金额": "NextFirstPrizePool",
        "本期兑奖截止日": "RedemptionDeadline",
        "总注数": "TotalBets",
        "detailsLink": "DetailsLink",
        "detailsNum": "DetailsNumber"
    }
    df.rename(columns=mapping, inplace=True)
    return df


def convert_week(df):
    """将 Week 列的中文星期转换为数字（1-7）"""
    mapping = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}
    if "Week" in df.columns:
        df["Week"] = df["Week"].map(mapping)
    return df


def fill_redemption_deadline(df):
    """
    补齐缺失的 RedemptionDeadline 值：如果该字段为空，
    则以 DrawDate 为基准，加两个月减一天，格式化为 YYYY-MM-DD。
    """

    def get_deadline(row):
        rd = row.get("RedemptionDeadline")
        if pd.isna(rd) or str(rd).strip() == "":
            draw_date = row.get("DrawDate")
            try:
                dt = pd.to_datetime(draw_date, errors='coerce')
                if pd.isna(dt):
                    return ""
                new_dt = dt + relativedelta(months=+2) - pd.Timedelta(days=1)
                return new_dt.strftime("%Y-%m-%d")
            except Exception as e:
                return ""
        else:
            try:
                dt = pd.to_datetime(rd, errors='coerce')
                if pd.isna(dt):
                    return rd
                return dt.strftime("%Y-%m-%d")
            except Exception as e:
                return rd

    df["RedemptionDeadline"] = df.apply(get_deadline, axis=1)
    return df


def convert_text_columns(df):
    """
    对部分文本列进行转换，例如保持 FirstWinningRegions 不变（按要求不动）。
    """
    # 这里如果需要额外转换，可添加转换逻辑，本示例不对 FirstWinningRegions 进行处理
    return df


def remove_irrelevant_features(df):
    """
    删除对 AI 建模没有意义的字段，
    同时从 DetailsLink 中提取 DetailsNumber（确保 DetailsLink 为字符串）。
    """
    if "DetailsLink" in df.columns:
        df["DetailsLink"] = df["DetailsLink"].astype(str)
        df["DetailsNumber"] = df["DetailsLink"].str.extract(r'/(\d+)\.shtml')[0]
    cols_to_drop = [
        "Name",  # 常量，如始终为“双色球”
        "VideoLink",  # URL字段
        "Blue2",  # 缺失率高
        "Content",  # 描述性文本
        "AddMoney",  # 缺失率高
        "AddMoney2",  # 缺失率高
        "Message",  # 缺失率高
        "Z2Add",  # 缺失率高
        "M2Add",  # 缺失率高
        "Date"  # 与 DrawDate 重复
    ]
    # 删除地域分布的字段
    region_columns = [
        "上海", "云南", "内蒙古", "北京", "吉林", "四川", "天津", "宁夏",
        "安徽", "山东", "山西", "广东", "广西", "新疆", "江苏", "江西",
        "河北", "河南", "浙江", "海南", "深圳", "湖北", "湖南",
        "甘肃", "福建", "西藏", "贵州", "辽宁", "重庆", "陕西", "青海", "黑龙江"
    ]
    cols_to_drop.extend(region_columns)
    cols_to_drop = [col for col in cols_to_drop if col in df.columns]
    df_clean = df.drop(columns=cols_to_drop)
    return df_clean


##############################################
# 主程序：加载、二次清洗与保存
##############################################
def main():
    # 1. 加载原始数据
    df = load_data("1.merged_output_cleaned.csv")
    print("初始数据形状：", df.shape)

    # 2. 删除“WinningNumbers”（或“开奖号码”）列
    df = drop_winning_numbers(df)
    print("删除WinningNumbers后形状：", df.shape)

    # 3. 重命名列（中文转英文）
    df = rename_columns(df)

    # 4. 将 Week 列转换为数字
    df = convert_week(df)

    # 5. 补齐缺失的 RedemptionDeadline（先转 DrawDate + 2月 - 1天），再转换格式
    df = fill_redemption_deadline(df)

    # 6. 对其他文本列转换（如 FirstWinningRegions 保持原样，这里不做处理，可根据需要添加）
    df = convert_text_columns(df)

    # 7. 删除无意义的字段，并提取 DetailsNumber
    df = remove_irrelevant_features(df)

    # 先将 FirstWinningCount 和 FirstWinningAmount 中的空字符串替换成 NaN，
    # 再转换为数值类型后填充默认值

    df["FirstWinningCount"] = pd.to_numeric(df["FirstWinningCount"].replace("", pd.NA), errors='coerce').fillna(1)
    df["FirstWinningAmount"] = pd.to_numeric(df["FirstWinningAmount"].replace("", pd.NA), errors='coerce').fillna(1000000)

    # 如果 "SeventhPrizeCount" 和 "SeventhPrizeAmount" 两列全部为空，则删除这两列
    if df["SeventhPrizeCount"].isnull().all() and df["SeventhPrizeAmount"].isnull().all():
        df = df.drop(columns=["SeventhPrizeCount", "SeventhPrizeAmount"])

    # 保存最终清洗后的数据
    df.to_csv("1.5merged_output_final_cleaned.csv", index=False, encoding="utf-8")
    print("已保存最终清洗后的数据到 1.5merged_output_final_cleaned.csv")


if __name__ == "__main__":
    main()
