#!/usr/bin/env python
# coding=utf-8
import math
import sys
import gc
from datetime import datetime, timedelta

if len(sys.argv) <= 7:
    print '参数说明: 间隔时间 interval, 平稳阈值 stable, 突破阈值 break, 平稳时间 silence, 买入追踪时间 limitation, 最小上涨幅度 gate, 最大回撤容忍 torlance'
    exit()
#################################
# 读取 etf 50 数据
#################################

etf_50_file = open("etf_50_nearby.txt")
etf = []

for line in etf_50_file:
    item = {}
    line = line.split('\n')[0]
    split_line = line.split(',')
    date = datetime.strptime(split_line[0], '%Y-%m-%d %H:%M:%S')
    # time_info =  date.strftime('%Y-%m-%d %H:%M:%S')
    item['time'] = date
    item['price_open'] = float(split_line[1])
    item['price_high'] = float(split_line[2])
    item['price_low'] = float(split_line[3])
    item['price_close'] = float(split_line[4])
    item['price'] = (item['price_open'] + item['price_close'])/2
    item['bonus_rate'] = (item['price_close'] -  item['price_open'])/item['price_open']
    gc.disable()
    etf.append(item)
    gc.enable()


###################################
# 读取离岸人民币数据
###################################

ovc_rmb_file = open("ovc_rmb_nearby.txt")
rmb = []

for line in ovc_rmb_file:
    item = {}
    line = line.split('\n')[0]
    split_line = line.split(',')
    date = datetime.strptime(split_line[0], '%Y-%m-%d %H:%M')
    # time_info = date.strftime('%Y-%m-%d %H:%M:%S')
    item['time'] = date
    item['price_open'] = float(split_line[2])
    item['price_high'] = float(split_line[3])
    item['price_low'] = float(split_line[4])
    item['price_close'] = float(split_line[5])
    item['price'] = (item['price_open'] + item['price_close'])/2
    item['bonus_rate'] = (item['price_close'] -  item['price_open'])/item['price_open']
    gc.disable()
    rmb.append(item)
    gc.enable()


# datetime.datetime.noyyw()+datetime.timedelta(minutes=1)

####################################
# 获取所有的突破点位置
####################################
'''
total_num = 0
total_rate = 0
abs_total_rate = 0
max_total_rate = 0
for item in rmb:
    total_num = total_num + 1
    total_rate = item['bonus_rate']
    abs_total_rate = abs(item['bonus_rate'])
    max_total_rate = item['bonus_rate'] if item['bonus_rate'] > max_total_rate else max_total_rate


print 'total_rate', total_rate / total_num
print 'abs_total_rate', abs_total_rate / total_num
print 'max_total_rate', max_total_rate 
'''

# max_total_rate 是 0.003，也就是千分之三，我们设定突破阈值为 0.0005，平稳阈值为 0.0001
'''
break_rate = 0.0005 # 突破阈值
stable_rate = 0.0002 # 平稳阈值
silence_time = 10 # 平稳最短时间，暂时设定为 30 min 


break_num = 0
stable_num = 0
total_num = 0
for item in rmb:
    total_num = total_num + 1
    if item['bonus_rate'] > break_rate:
        break_num = break_num + 1
    if item['bonus_rate'] > stable_rate:
        stable_num = stable_num + 1

print 'total_num: ', total_num
print 'break_num: ', break_num
print 'stable_num: ', stable_num


index = 0
for item in rmb:
    if item['bonus_rate'] > break_rate:
        # print '============'
        # print 'break point: ', item['time'], item['bonus_rate']
        buy_in = 1
        for i in xrange(0, silence_time):
            if index < silence_time:
                buy_in = 0
                # print 'unuse point: no enough history'
                break
            if rmb[index -i -1]['time'] != (item['time'] - timedelta(minutes=i+1)):
                buy_in = 0
                # print 'unuse point: time not match', rmb[index -i]['time'], item['time'] - timedelta(minutes=i+1)
                break
            if abs(rmb[index -i -1]['bonus_rate']) > stable_rate:
                buy_in = 0
                # print 'unuse point: no enough silence', rmb[index -i -1]['bonus_rate']
                break
        # if buy_in:
            # print 'buyin point: ', item['time'], item
    index = index + 1
'''
#################################
# 根据最小步长计算收益和突破
#################################
interval = 2 # 最小步长，单位 min
interval = int(sys.argv[1])
# 离岸人民币数据 rmb
# etf 50 数据 etf

rmb_interval = []
index = 0
item_interval = {}
# print 'rmb', len(rmb)
for item in rmb:
    index = index if index < interval else 0

    if index == 0:
        item_interval = {}
        item_interval['time'] = item['time']
        item_interval['price_open'] = item['price_open']
        item_interval['price_high'] = item['price_high']
        item_interval['price_low'] = item['price_low']
        # print 'item_interval', item_interval

    item_interval['price_high'] = item['price_high'] if item['price_high'] > item_interval['price_high'] else item_interval['price_high']
    item_interval['price_low'] = item['price_low'] if item['price_low'] < item_interval['price_low'] else item_interval['price_low']

    if index == interval - 1:
        item_interval['price_close'] = item['price_close']
        item_interval['bonus_rate'] = (item['price_close'] -  item['price_open'])/item['price_open']
        rmb_interval.append(item_interval)

    index = index + 1


# print 'rmb_interval', len(rmb_interval)

################################################
# 带间隔的突破点计算 
################################################


break_rate = 0.0005 # 突破阈值
stable_rate = 0.0001 # 平稳阈值
silence_time = 1 # 平稳最短时间，是 interval 的个数 

stable_rate = float(sys.argv[2])
break_rate = float(sys.argv[3])
silence_time = int(sys.argv[4])

buyin = {}
index = 0
for item in rmb_interval:
    if item['bonus_rate'] > break_rate:
        # print '============'
        # print 'break point: ', item['time'], item['bonus_rate']
        buy_in = 1
        for i in xrange(0, silence_time):
            if index < silence_time:
                buy_in = 0
                # print 'unuse point: no enough history'
                break
            if rmb_interval[index -i - 1]['time'] != (item['time'] - timedelta(minutes=(i+1) * interval)):
                buy_in = 0
                # print 'item.time', item['time']
                # print 'unuse point: time not match', rmb_interval[index -i -1]['time'], item['time'] - timedelta(minutes=(i+1) * interval)
                break
            if abs(rmb_interval[index -i -1]['bonus_rate']) > stable_rate:
                buy_in = 0
                # print 'unuse point: no enough silence', rmb_interval[index -i -1]['bonus_rate']
                break
        if buy_in:
            # print 'buyin point: ', item['time'], item
            # print item['time']
            gc.disable()
            buyin[item['time']] = True
            gc.enable()
    index = index + 1

#######################################
# 根据 buyin 买入时间来买入和计算收益
#######################################

limitation = 30 # 等待涨幅的时长
gate = 0.003 # 预期收益率
torlence = 0.003 # 能够忍受的最大回撤

limitation = int(sys.argv[5])
gate = float(sys.argv[6])
torlence = float(sys.argv[7])

success_num = 0
lost_num = 0
fail_num = 0

index = 0
for item in etf:
    # 如果符合条件则买入
    if buyin.has_key(item['time']):
        price_open = 0
        price_close = 0
        success = 0
        # 从下一秒开始买入，所以需要 +1
        for i in xrange(index + 1, index + limitation + 1):
            # print i
            if index + limitation + 1 > len(etf):
                success = 2
                fail_num = fail_num + 1
                print 'etf buy fail, not enough data', item['time'] 
                break
            if etf[i]['time'] != (item['time'] + timedelta(minutes=(i - index))):
                success = 2
                fail_num = fail_num + 1
                print 'etf buy fail, time not match:', etf[i]['time'], item['time'] + timedelta(minutes=(i - index))
                break
            if i == index + 1:
                price_open = etf[i]['price_open']
            price_close = etf[i]['price_close']
            bonus_rate = (price_close - price_open)/ price_open
            if bonus_rate > gate:
                success = 1
                success_num = success_num + 1
                print 'etf buy bouns, rate = ', bonus_rate, item['time'], etf[i]['time']
                print '买入价格', price_open
                print '卖出价格', price_close
                print '买入时间点信息', etf[index + 1]
                print '卖出时间点信息', etf[i]
                break
            if bonus_rate < -torlence:
                success = 2
                lost_num = lost_num + 1
                print 'etf buy loss, out of torlence, rate = ', bonus_rate, item['time']
                break
        if success == 0:
            lost_num = lost_num + 1
            print 'etf buy loss, rate is note enough, rate = ', bonus_rate, item['time']
    index = index + 1

print 'interval', interval,
print 'stable_rate', stable_rate,
print 'break_rate', break_rate,
print 'silence_time', silence_time,
print 'limitation', limitation,
print 'gate', gate,
print 'torlence', torlence,
print 'success_rate', float(success_num)/(success_num + lost_num + 0.000000000001),
print 'operation_num', success_num +  lost_num

'''
total_bonus = 0 
max_bonus = 0
index = 1
for item in etf:
    total_bonus = abs(item['bonus_rate'])
    index = index  + 1
    max_bonus = max_bonus if abs(item['bonus_rate']) < max_bonus else abs(item['bonus_rate'])

print total_bonus / index, max_bonus
'''


















