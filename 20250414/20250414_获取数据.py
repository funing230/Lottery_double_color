import requests
import json
import csv
import time

def get_ssq_data():
    """
    翻页获取数据，加入更多请求头，使用 Session 对象，
    并利用每条记录的 'code' 字段去重，避免重复数据。
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Referer': 'https://www.cwl.gov.cn/ygkj/kjgg/',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.cwl.gov.cn'
    })

    base_url = 'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice'
    params = {
        'name': 'ssq',
        'issuecount': '',
        'issuestart': '',
        'issueend': '',
        'daystart': '',
        'dayend': '',
        'pageno': 1,
        'pagesize': 30,
        'week': '',
        'systemtype': 'pc'
    }

    unique_data = {}  # 以 code 为键，实现去重
    while True:
        response = session.get(base_url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"请求第 {params['pageno']} 页时出错：{e}")
            break

        data_json = response.json()
        page_data = data_json.get("result", [])
        if not page_data:
            break

        # 遍历当前页数据，根据 code 去重
        for item in page_data:
            code = item.get("code")
            if code not in unique_data:
                unique_data[code] = item

        # 当当前页返回的数据条数不足 pagesize，认为达到最后一页
        if len(page_data) < params['pagesize']:
            break
        params['pageno'] += 1
        time.sleep(1)

    return list(unique_data.values())

def parse_ssq_data(data):
    """
    解析数据时将原始 JSON 中的所有键（除了 prizegrades）复制至记录，
    并对 prizegrades 数组进行扁平化处理，保留所有字段信息。
    """
    result = []
    for item in data:
        # 复制除 prizegrades 外的所有键
        record = { key: item.get(key, "") for key in item if key != "prizegrades" }
        # 对 "red" 字段进行格式化，将逗号替换为空格
        if "red" in record:
            record["red"] = record["red"].replace(',', ' ')
        # 扁平化 prizegrades 数组，将奖项信息存入对应字段
        prizegrades = item.get("prizegrades", [])
        for prize in prizegrades:
            prize_type = prize.get("type")
            typenum = prize.get("typenum", "")
            typemoney = prize.get("typemoney", "")
            # 根据奖项类型确定生成的字段名
            if prize_type == 1:
                key_num = "一等奖注数"
                key_money = "一等奖金额"
            elif prize_type == 2:
                key_num = "二等奖注数"
                key_money = "二等奖金额"
            elif prize_type == 3:
                key_num = "三等奖注数"
                key_money = "三等奖金额"
            else:
                key_num = f"奖项{prize_type}注数"
                key_money = f"奖项{prize_type}金额"
            record[key_num] = typenum
            record[key_money] = typemoney
        result.append(record)
    return result

def main():
    data = get_ssq_data()
    parsed_data = parse_ssq_data(data)

    # 动态获取所有 CSV 表头（所有键的并集），确保包含所有字段
    fieldnames = set()
    for item in parsed_data:
        fieldnames.update(item.keys())
    # 固定顺序字段（也可根据需要调整顺序）
    fixed_order = [
        "name", "code", "detailsLink", "videoLink", "date", "week",
        "red", "blue", "blue2", "sales", "poolmoney", "content",
        "addmoney", "addmoney2", "msg", "z2add", "m2add",
        "一等奖注数", "一等奖金额", "二等奖注数", "二等奖金额", "三等奖注数", "三等奖金额"
    ]
    remaining = sorted(fieldnames - set(fixed_order))
    final_fieldnames = fixed_order + remaining

    with open('ssq_winning_records_all.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=final_fieldnames)
        writer.writeheader()
        for item in parsed_data:
            writer.writerow(item)

if __name__ == "__main__":
    main()
