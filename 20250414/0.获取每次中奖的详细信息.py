import requests
import csv
import time
from bs4 import BeautifulSoup

def get_details(url, session):
    """
    访问详情页面，返回页面提取的文本内容。
    你可以根据页面的实际结构修改 selector 提取更具体的信息。
    """
    try:
        response = session.get(url)
        response.raise_for_status()
        html = response.content
        # 使用 BeautifulSoup 解析页面
        soup = BeautifulSoup(html, "html.parser")
        # 这里可以根据实际情况修改提取内容，比如：
        # detail_div = soup.find("div", class_="article")
        # 如果找到则返回其文本，否则返回整个页面文本
        detail_text = soup.get_text(separator="\n", strip=True)
        return detail_text
    except Exception as e:
        print(f"获取 {url} 出错: {e}")
        return ""

def main():
    input_csv = "ssq_winning_records_all.csv"  # 源数据文件（包含 detailsLink 字段）
    output_csv = "0.ssq_details_info.csv"          # 保存详情爬取结果的文件

    # 初始化 Session 并设置请求头
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Referer': 'https://www.cwl.gov.cn',
    })

    records = []
    # 读取输入 CSV 文件
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 期号作为唯一标识
            code = row.get("code") or row.get("期号", "")
            # 获取详情链接（字段名取决于你保存时的键，此处取 "detailsLink"）
            details_link = row.get("detailsLink") or row.get("详情链接", "")
            if details_link:
                # 如果 details_link 为相对链接，则加上域名
                if details_link.startswith("/"):
                    full_url = "https://www.cwl.gov.cn" + details_link
                else:
                    full_url = details_link
                print(f"获取期号 {code} 的详情页：{full_url}")
                detail_info = get_details(full_url, session)
                records.append({"code": code, "detailsLink": full_url, "detail_info": detail_info})
                # 延时 1 秒，防止请求过快
                time.sleep(1)

    # 写入结果到输出 CSV 文件
    fieldnames = ["code", "detailsLink", "detail_info"]
    with open(output_csv, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print("所有详情信息已保存到", output_csv)

if __name__ == "__main__":
    main()
