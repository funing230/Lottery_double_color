import requests
import json
import csv


def get_ssq_data():
    url = 'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issuecount=&issuestart=&issueend=&daystart=&dayend=&pageno=1&pagesize=30&week=&systemtype=pc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Referer': 'https://www.cwl.gov.cn/ygkj/kjgg/'
    }
    response = requests.get(url, headers=headers)
    data_json = response.json()
    return data_json["result"]


def parse_ssq_data(data):
    result = []
    for item in data:
        code = item["code"]
        date = item["date"]
        red = item["red"].replace(',', ' ')
        blue = item["blue"]
        prizegrades = item["prizegrades"]
        prize_info = {}
        for prize in prizegrades:
            prize_type = prize["type"]
            prize_name = "一等奖" if prize_type == 1 else "二等奖" if prize_type == 2 else "三等奖" if prize_type == 3 else "其他奖项"
            typenum = prize["typenum"]
            typemoney = prize["typemoney"]
            if prize_type in [1, 2, 3] and typenum and typemoney:
                prize_info[prize_name] = {
                    "注数": typenum,
                    "金额": typemoney,
                }
        result.append({
            "期号": code,
            "开奖日期": date,
            "红球": red,
            "蓝球": blue,
            **prize_info
        })
    return result


def main():
    data = get_ssq_data()
    parsed_data = parse_ssq_data(data)

    # 指定CSV文件的列名（表头）
    fieldnames = ["期号", "开奖日期", "红球", "蓝球", "一等奖注数", "一等奖金额", "二等奖注数", "二等奖金额", "三等奖注数", "三等奖金额"]
    with open('ssq_winning_records.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入表头
        writer.writeheader()

        # 逐行写入数据
        for item in parsed_data:
            row_data = {
                "期号": item["期号"],
                "开奖日期": item["开奖日期"],
                "红球": item["红球"],
                "蓝球": item["蓝球"],
                "一等奖注数": item.get("一等奖", {}).get("注数", ""),
                "一等奖金额": item.get("一等奖", {}).get("金额", ""),
                "二等奖注数": item.get("二等奖", {}).get("注数", ""),
                "二等奖金额": item.get("二等奖", {}).get("金额", ""),
                "三等奖注数": item.get("三等奖", {}).get("注数", ""),
                "三等奖金额": item.get("三等奖", {}).get("金额", "")
            }
            writer.writerow(row_data)


if __name__ == "__main__":
    main()