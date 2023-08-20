#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/11/16 19:35:00
# @Email : jtyoui@qq.com
# @Software : PyCharm
"""爬取福利彩票官方双色球数据"""
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pprint


def double_data_chart(start: str = None, end: str = None):
    """爬取双色球数据

    :param start: 开始期号：默认是最早的一期
    :param end:   结束期号：默认是最新的一期
    :return: 二维列表: '红1', '红2', '红3', '红4', '红5', '红6', '篮球'
    """
    header, charts = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '篮球','奖池奖金(元)','一等奖 注数','一等奖 奖金(元)','二等奖 注数','二等奖 奖金(元)','总投注额(元)','开奖日期'], []
    url = 'https://datachart.500.com/ssq/history/newinc/history.php'
    start = start or '03001'
    if end is None:
        text = requests.get(url=url, params={'user-agent': UserAgent().random}).text
        soup = BeautifulSoup(text, 'html.parser')
        end = soup.find(name='input', id='end').get('value')
    reptile_url = url + f'?start={start}&end={end}'
    text = requests.get(url=reptile_url, params={'user-agent': UserAgent().random}).text
    soup = BeautifulSoup(text, 'html.parser')
    for data in soup.find_all(name='tr', class_='t_tr1'):
        ls = [int(content.text) for content in data.contents[1:9]]
        total_money=data.contents[10].text  #奖池奖金(元)
        fist_number=data.contents[11].text  #一等奖 注数
        first_money=data.contents[12].text  #一等奖 奖金(元)
        second_number=data.contents[13].text  #	二等奖 注数
        second_money=data.contents[14].text  #	二等奖 奖金(元)
        total_input_money=data.contents[15].text  #总投注额(元)
        date=data.contents[16].text  #开奖日期
        ls.append(total_money)
        ls.append(fist_number)
        ls.append(first_money)
        ls.append(second_number)
        ls.append(second_money)
        ls.append(total_input_money)
        ls.append(date)
        charts.append(ls)
    charts.reverse()
    charts.insert(0, header)
    return charts


if __name__ == '__main__':
    charts=double_data_chart()
    # pprint.pprint(charts)
    columns = charts[0]
    data = charts[1:]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("double_colors.csv", index=False)
    # 打印DataFrame
    print(df)


def double_data_chart_old(start: str = None, end: str = None):
    """爬取双色球数据

    :param start: 开始期号：默认是最早的一期
    :param end:   结束期号：默认是最新的一期
    :return: 二维列表: '红1', '红2', '红3', '红4', '红5', '红6', '篮球'
    """
    header, charts = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '篮球'], []
    url = 'https://datachart.500.com/ssq/history/newinc/history.php'
    start = start or '03001'
    if end is None:
        text = requests.get(url=url, params={'user-agent': UserAgent().random}).text
        soup = BeautifulSoup(text, 'html.parser')
        end = soup.find(name='input', id='end').get('value')
    reptile_url = url + f'?start={start}&end={end}'
    text = requests.get(url=reptile_url, params={'user-agent': UserAgent().random}).text
    soup = BeautifulSoup(text, 'html.parser')
    for data in soup.find_all(name='tr', class_='t_tr1'):
        ls = [int(content.text) for content in data.contents[1:9]]
        charts.append(ls)
    charts.reverse()
    charts.insert(0, header)
    return charts