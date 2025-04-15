import pandas as pd
import re
import csv


def extract_region_info(text):
    """
    从文本中提取中奖区域信息，匹配类似“北京1注”的格式，
    返回字典，键为区域名称，值为中奖注数；若有“共XX注”或“合计XX注”，存为 "总注数"。
    """
    region_pattern = re.compile(r'([\u4e00-\u9fa5]+)(\d+)注')
    matches = region_pattern.findall(text)
    info = {}
    for region, count in matches:
        if region in ['共', '合计']:
            info["总注数"] = int(count)
        else:
            info[region] = int(count)
    return info


def extract_features_from_detail(text):
    """
    根据详情文本中的格式，从中提取有用的特征信息，采用多行模式。
    返回一个字典，字段包括：
      - 开奖日期
      - 本期销售金额
      - 开奖号码
      - 各奖项中奖注数与单注中奖金额（一等奖至六等奖）
      - 一等奖中奖情况（区域中奖信息，后续分解为各省数据）
      - 下期一等奖奖池累计金额
      - 本期兑奖截止日
    """
    features = {}

    # 确保输入为字符串
    if not isinstance(text, str):
        text = str(text)

    # 开奖日期：匹配行首“开奖日期：”后面的内容
    m = re.search(r'^开奖日期[：:]\s*(.+)$', text, re.MULTILINE)
    features["开奖日期"] = m.group(1).strip() if m else ""

    # 本期销售金额：匹配“本期销售金额”或“本期销售额”后的数字，去掉逗号
    m = re.search(r'^本期销售(?:金额|额)[：:]\s*([\d,]+)元', text, re.MULTILINE)
    features["本期销售金额"] = m.group(1).replace(",", "") if m else ""

    # 开奖号码：匹配“开奖号码”后面的所有文本直到“中奖情况”
    m = re.search(r'开奖号码[：:]\s*(.*?)\s*中奖情况', text, re.DOTALL)
    if m:
        lines = [line.strip() for line in m.group(1).splitlines() if line.strip()]
        if lines and all(line == "-" for line in lines):
            features["开奖号码"] = " ".join(lines)
        else:
            valid_lines = [line for line in lines if line != "-"]
            features["开奖号码"] = " ".join(valid_lines)
    else:
        features["开奖号码"] = ""

    # 提取各奖项数据：针对一等奖到六等奖
    prize_levels = ["一等奖", "二等奖", "三等奖", "四等奖", "五等奖", "六等奖"]
    for level in prize_levels:
        # 利用多行模式，奖项名称行后紧跟中奖注数和单注中奖金额的两行
        pattern = r'^' + level + r'\s*[\r\n]+(\d+)\s*[\r\n]+(\d+)\s*$'
        m = re.search(pattern, text, re.MULTILINE)
        if m:
            features[f"{level}中奖注数"] = m.group(1)
            features[f"{level}单注中奖金额"] = m.group(2)
        else:
            features[f"{level}中奖注数"] = ""
            features[f"{level}单注中奖金额"] = ""

    # 提取一等奖中奖情况（区域）
    m = re.search(r'^一等奖中奖情况[：:]\s*(.+)$', text, re.MULTILINE)
    if m:
        region_str = m.group(1).strip()
        features["一等奖中奖情况"] = region_str
        # 假设 extract_region_info 函数已定义，用于进一步分解区域信息
        region_info = extract_region_info(region_str)
        features.update(region_info)
    else:
        features["一等奖中奖情况"] = ""

    # 下期一等奖奖池累计金额
    m = re.search(r'^下期一等奖奖池累计金额[：:]\s*([\d,]+)元', text, re.MULTILINE)
    features["下期一等奖奖池累计金额"] = m.group(1).replace(",", "") if m else ""

    # 本期兑奖截止日
    m = re.search(r'^本期兑奖截止日为\s*([\d年月日]+)', text, re.MULTILINE)
    features["本期兑奖截止日"] = m.group(1).strip() if m else ""

    return features


def process_details(input_csv="0.ssq_details_info.csv", output_csv="0.5ssq_details_extracted.csv"):
    """
    从输入 CSV（应包含 code、detailsLink 与 detail_info 字段）中读取数据，
    对每条记录的 detail_info 文本调用 extract_features_from_detail() 提取特征，
    并将 code、detailsLink 与所有提取出的特征保存到新的 CSV 文件中。
    """
    df = pd.read_csv(input_csv, encoding="utf-8")
    extracted_data = []

    for idx, row in df.iterrows():
        code = row.get("code", "")
        details_link = row.get("detailsLink", "")
        detail_info = row.get("detail_info", "")
        features = extract_features_from_detail(detail_info)
        record = {"code": code, "detailsLink": details_link}
        record.update(features)
        extracted_data.append(record)

    # 动态收集所有字段
    fieldnames = set()
    for item in extracted_data:
        fieldnames.update(item.keys())
    # 固定顺序字段（根据需求可调整顺序）
    fixed_order = [
        "code", "detailsLink", "开奖日期", "本期销售金额", "开奖号码",
        "一等奖中奖注数", "一等奖单注中奖金额",
        "二等奖中奖注数", "二等奖单注中奖金额",
        "三等奖中奖注数", "三等奖单注中奖金额",
        "四等奖中奖注数", "四等奖单注中奖金额",
        "五等奖中奖注数", "五等奖单注中奖金额",
        "六等奖中奖注数", "六等奖单注中奖金额",
        "一等奖中奖情况", "下期一等奖奖池累计金额", "本期兑奖截止日"
    ]
    remaining = sorted(fieldnames - set(fixed_order))
    final_fieldnames = fixed_order + remaining

    output_df = pd.DataFrame(extracted_data)
    output_df = output_df.reindex(columns=final_fieldnames)
    output_df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"已保存提取的详细特征信息到 {output_csv}")


def main():
    process_details()


if __name__ == "__main__":
    main()
