import pandas as pd
from decimal import Decimal, getcontext
from datetime import datetime, timedelta
# 读取CSV文件
data = pd.read_csv("double_colors.csv",  parse_dates=['开奖日期'],index_col='开奖日期')

current_date = datetime.today().date()
# 计算一周前的日期
one_week_ago = current_date - timedelta(days=3650)
# 计算一个月前的日期
one_month_ago = current_date - timedelta(days=30)




# 提取最初十次开奖的红色号码数据
red_numbers1 = data["红1"].loc[one_week_ago:current_date] # 假设红色号码的列名为 "红1"
red_numbers2 = data["红2"].loc[one_week_ago:current_date]
red_numbers3 = data["红3"].loc[one_week_ago:current_date]
red_numbers4 = data["红4"].loc[one_week_ago:current_date]
red_numbers5 = data["红5"].loc[one_week_ago:current_date]
red_numbers6 = data["红6"].loc[one_week_ago:current_date]

blue_number =data['篮球'].loc[one_week_ago:current_date]
# 统计红色号码等于1的次数
rednumber=5
bluenumber=15
getcontext().prec = 300
count_red_1 = red_numbers1[red_numbers1 == rednumber].count()
count_red_2 = red_numbers2[red_numbers2 == rednumber].count()
count_red_3 = red_numbers3[red_numbers3 == rednumber].count()
count_red_4 = red_numbers4[red_numbers4 == rednumber].count()
count_red_5 = red_numbers5[red_numbers5 == rednumber].count()
count_red_6 = red_numbers6[red_numbers6 == rednumber].count()
# 计算概率
count_red=count_red_1 +count_red_2 +count_red_3 +count_red_4 +count_red_5 +count_red_6
count_red = int(count_red)
probability = Decimal(count_red) / Decimal(data.__len__())

print(f"红色号码等于{rednumber}在最初十次开奖中出现的概率为：{probability:.300f}")

probability =  (count_red) / (data.__len__())

print(f"红色号码等于{rednumber}在最初十次开奖中出现的概率为：{probability:.300f}")

#0.00065832784726793943383805134957

# 获取当前日期
# 0.000658327847267939433838051349572086899275839368005266622778143515470704410796576695194206714944042132982225148123765635286372613561553653719552337063857801184990125082290980908492429229756418
#0.00065832784726793943383805134957208689927583936800526662277814351547070441079657669519420671494404213298222514812376563528637261356155365371955233706385780


# 截取一周内的数据
data_one_week = data.loc[one_week_ago:current_date]

# 截取一个月内的数据
data_one_month = data.loc[one_month_ago:current_date]