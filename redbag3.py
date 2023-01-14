from collections import Counter
import heapq
import itertools
from pprint import pprint
import random
from matplotlib import pyplot as plt
import numpy as np

all_red_bag = 10
all_red_bag_money = 20
remain_money = all_red_bag_money
remain_red_bag = all_red_bag
# 每个次序抢到的金额
all_money_list = []
# 循环次数
loop = 1000

# ---阈值设置---
# 当前上水位超过多少倍平均上水位
water_rate = 1.5
# 出现下水位的概率小于几
water_bottom_rate = 20
# 没有出现多少倍上水位红包
no_how_rate_top = 1
# 没有出现过大于多少的红包
no_appearance = 2

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

    # 计算余数为0或0.01的概率
    # probably_list = []
    # for i in np.arange(water_bottom, water_top+water_bottom, water_bottom):
    #     if water_top % i == 0 or abs(water_top%i-0.01)<1e-5:
    #         probably_list.append(i)

    # 根据余数计算红包金额
    if water_remainder > water_bottom:
        current_money = water_radom
    else:
        current_money = water_bottom

    # 打印数据
    # print("当前是第:{}个, 余数是:{}, 上水位是:{}, 随机数是:{}, 余数为0的概率是:{}, 值是:{}".format(all_red_bag-remain_red_bag+1,
    #                                                                             water_remainder,
    #                                                                             water_top,
    #                                                                             water_radom,
    #                                                                             len(probably_list),
    #                                                                             current_money
    #                                                                             ))
    # print(                                                                      all_red_bag-remain_red_bag+1,
    #                                                                             water_remainder,
    #                                                                             water_top,
    #                                                                             water_radom,
    #                                                                             # len(probably_list),
    #                                                                             current_money)

    # 返回当前红包金额
    return current_money

def if_unpack_red_bag(remain_money,remain_red_bag,sub_money_list):
    # 第一个和第二个包都不开 前三个包都不开了！
    if remain_red_bag == all_red_bag or remain_red_bag+1 == all_red_bag or remain_red_bag+2 == all_red_bag:
        return False,0,[0]

    # 1. 如果当前上水位超过1/2平均上水位就标记
    if_over_half_water = 0
    # 2. 如果当前为0.01的几率小于5就标记
    if_less_bottom = 0
    # 3. 如果没有出现超过1/2上水位的红包数量就标记
    if_appearance_half_water = 0
    # 4. 没出现过指定红包
    if_no_app = 0
    # 超过两个标记就拆开红包

    # 判断1
    water_bottom = 0.01
    water_top1 = round(remain_money / remain_red_bag * 2,2)
    water_top2 = round(remain_money - round(water_bottom*(remain_red_bag-1),2),2)
    water_top = min(water_top1,water_top2)
    water_average = all_red_bag_money/all_red_bag
    if water_top > water_average*water_rate:
        if_over_half_water = 1
    
    # 判断2
    probably_list = []
    for i in np.arange(water_bottom, water_top+water_bottom, water_bottom):
        if water_top % i == 0 or abs(water_top%i-0.01)<1e-5:
            probably_list.append(i)
    if len(probably_list)<water_bottom_rate:
        if_less_bottom = 1

    # 判断3
    if max(sub_money_list) < water_average*no_how_rate_top:
        if_appearance_half_water = 1

    # 判断4 
    for i in sub_money_list:
        if no_appearance > i:
            if_no_app = 1

    conditions = [if_appearance_half_water, if_less_bottom, if_over_half_water, if_no_app]

    # check if at least 2 conditions are met
    for c in itertools.combinations(conditions, 4):
        if all(c):
            return True,water_top,probably_list

    # 如果当前只剩最后一个红包了直接开
    if remain_red_bag == 1:
        return True,0,[0]
    
    return False,0,[0]

def generate_red_bag_list(loop):
    """
    循环生成抢红包金额链
    """
    for i in range(loop):

        # 记录我拆的红包和金额
        my_red_bag = True # True表示这轮还没拆
        my_red_bag_money = 0

        # 外层重定义剩余
        remain_money = all_red_bag_money
        remain_red_bag = all_red_bag

        # 当前小结金额链
        sub_money_list = []

        # 进入循环开始抢红包并记录money_list
        for j in range(1,remain_red_bag+1):

            # 提前计算是否选中当前拆红包,当前论拆过就不拆了
            if  my_red_bag:
                # 计算拆不拆
                unpack_red_bag,water_top,remain_if = if_unpack_red_bag(remain_money,remain_red_bag,sub_money_list)
                # 返回True就拆
                if unpack_red_bag:
                    my_red_bag_money = all_red_bag - remain_red_bag
                    my_red_bag = False

            current_money = generate_red_bag(remain_money,remain_red_bag)

            # 重新计算剩余
            remain_money-=current_money
            remain_red_bag-=1
            sub_money_list.append(current_money)

        # 将我的红包添加到这轮红包链结尾，并判断我的红包是第几大的
        my_red_bag_money = sub_money_list[my_red_bag_money]
        sorted_list = sorted(sub_money_list, reverse=True)
        index = sorted_list.index(my_red_bag_money)
        rank = index + 1

        sub_money_list.append(my_red_bag_money)
        sub_money_list.append(rank)
        sub_money_list.append(water_top)
        sub_money_list.append(len(remain_if))

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

rank_list = []
for i in all_money_list:
    data = i[10]
    rank = i[11]
    top = i[12]
    rate = i[13]
    # print("当前红包:{} 排第{} 上水位是:{} 下水位概率是:{}".format(data,rank,top,rate))
    if rank<=3:
        rank_list.append(rank)
print(sum(rank_list)/loop)
