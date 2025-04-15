import pandas as pd
import re

# 定义中文省份到英文的映射字典
province_mapping = {
    "河北": "Hebei",
    "山西": "Shanxi",
    "上海": "Shanghai",
    "江苏": "Jiangsu",
    "浙江": "Zhejiang",
    "山东": "Shandong",
    "湖南": "Hunan",
    "广东": "Guangdong",
    "广西": "Guangxi",
    "四川": "Sichuan",
    "云南": "Yunnan",
    "辽宁": "Liaoning",
    "福建": "Fujian",
    "江西": "Jiangxi",
    "天津": "Tianjin",
    "内蒙古": "InnerMongolia",
    "吉林": "Jilin",
    "黑龙江": "Heilongjiang",
    "北京": "Beijing",
    "贵州": "Guizhou",
    "西藏": "Tibet",
    "宁夏": "Ningxia",
    "海南": "Hainan",
    "重庆": "Chongqing",
    "新疆": "Xinjiang"
}
# 按照字典中键的顺序构成省份列表
provinces = list(province_mapping.keys())

def parse_region_counts(region_str):
    """
    解析例如：
    "河北1注,山西1注,上海2注,江苏1注,浙江1注,山东3注,湖南1注,广东7注,广西1注,四川1注,云南1注,共20注。"
    返回 (counts_dict, total)，其中 counts_dict 为各省中奖注数字典，总注数 total 为数字。
    """
    region_str = region_str.strip("。")
    pattern = re.compile(r'([\u4e00-\u9fa5]+)(\d+)注')
    matches = pattern.findall(region_str)
    counts = {}
    total = None
    for region, count in matches:
        count = int(count)
        if region in ["共", "合计"]:
            total = count
        else:
            counts[region] = count
    if total is None:
        total = sum(counts.values())
    return counts, total

def row_region_probabilities(region_str):
    """
    对单行的 FirstWinningRegions 字符串返回一个字典，
    字典中键为英文省份名称（根据 province_mapping 转换），值为对应中奖注数/总注数的比例。
    """
    counts, total = parse_region_counts(region_str)
    prob_dict = {}
    for prov in provinces:
        cnt = counts.get(prov, 0)
        prob = cnt / total if total > 0 else 0
        eng_key = province_mapping[prov]
        prob_dict[eng_key] = prob
    return prob_dict

def process_first_winning_regions(region_str):
    """
    如果 region_str 非空，返回各省中奖概率字典；若为空，则所有省份概率设为 0。
    """
    if pd.isna(region_str) or region_str.strip() == "":
        return {province_mapping[prov]: 0 for prov in provinces}
    return row_region_probabilities(region_str)

# 读取源文件（请根据实际文件路径修改文件名）
df = pd.read_csv("1.5merged_output_final_cleaned.csv", encoding="utf-8")

# 遍历数据，每一行提取 code 和对应的各省中奖概率
result_rows = []
for idx, row in df.iterrows():
    code = row["Code"]
    region_str = row.get("FirstWinningRegions", "")
    prob_dict = process_first_winning_regions(region_str)
    prob_dict["code"] = code
    result_rows.append(prob_dict)

# 构造新的 DataFrame，列顺序为：code 加上各省英文名
columns_order = ["code"] + [province_mapping[prov] for prov in provinces]
df_prob = pd.DataFrame(result_rows, columns=columns_order)

# 保存结果到 CSV 文件
df_prob.to_csv("1.8processed_first_winning_regions_by_province.csv", index=False, encoding="utf-8")
print("已保存结果到 processed_first_winning_regions_by_province.csv")
