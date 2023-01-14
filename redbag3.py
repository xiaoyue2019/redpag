from collections import Counter
import heapq
import itertools
from pprint import pprint
import random
from matplotlib import pyplot as plt

all_red_bag = 10
all_red_bag_money = 20
remain_money = all_red_bag_money
remain_red_bag = all_red_bag
# 每个次序抢到的金额
all_money_list = []
# 循环次数
loop = 1

def generate_red_bag(remain_money,remain_red_bag):
    """
    剩余金额\n
    剩余红包数
    """
    if remain_money <= 0:
        exit("出错，剩余红包金额为0")
    if remain_red_bag == 1:
        return round(remain_money,2)
    
    # 计算上水位
    water_bottom = 0.01
    water_top1 = round(remain_money / remain_red_bag * 2,2)
    water_top2 = round(remain_money - round(water_bottom*(remain_red_bag-1),2),2)
    water_top = min(water_top1,water_top2)

    # 计算随机数和余数
    water_radom = round(random.uniform(water_bottom,water_top),2)
    water_remainder = round(water_top % water_radom,2)

    # 根据余数计算红包金额
    print("余数是:{}, 上水位是:{}, 随机数是:{}".format(water_remainder,water_top,water_radom))
    if water_remainder > water_bottom:
        current_money = water_radom
    else:
        current_money = water_bottom

    # 返回当前红包金额
    # print(water_top1,water_top2,current_money)
    return current_money

def generate_red_bag_list(loop):
    """
    循环生成抢红包金额链
    """
    for i in range(loop):
        # 外层重定义剩余
        remain_money = all_red_bag_money
        remain_red_bag = all_red_bag
        sub_money_list = []

        # 进入循环开始抢红包并记录money_list
        for j in range(1,remain_red_bag+1):
            current_money = generate_red_bag(remain_money,remain_red_bag)
            # 重新计算剩余
            remain_money-=current_money
            remain_red_bag-=1
            sub_money_list.append(current_money)

        # 将这一轮记录到总的money_list
        all_money_list.append(sub_money_list)

def calc_king_sum_data(loop):

    # 这里已经生成完了所有位置的money
    generate_red_bag_list(loop)

    # ---下面开始处理数据---
    king = []
    per_station_money = [0 for i in range(loop)]

    # 遍历二维数组即 所有位置的money
    for sublist in all_money_list:

        # 获取最大的三个数的下标
        top_three = heapq.nlargest(1, enumerate(sublist), key=lambda x: x[1])
        top_three_indices = [x[0]+1 for x in top_three]
        king.append(top_three_indices)

        # 将每个次序的数 分别相加 = 每个次序的红包和
        per_station_money = [round(x+y,2) for x, y in zip(per_station_money, sublist)]

    # 最大king 频次统计
    king_list = Counter([elem for sublist in king for elem in sublist])
    
    print(king_list,sorted(dict(zip([i for i in range(1,11)],per_station_money)).items(), key=lambda x: x[1],reverse=True),sep="\n")

generate_red_bag_list(loop)
print(all_money_list)