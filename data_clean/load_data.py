#!/usr/bin/env python
# coding=utf-8
import math
import gc
from datetime import datetime, timedelta

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

break_rate = 0.0005 # 突破阈值
stable_rate = 0.0002 # 平稳阈值
silence_time = 10 # 平稳最短时间，暂时设定为 30 min 

'''
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
'''

index = 0
for item in rmb:
    if item['bonus_rate'] > break_rate:
        print '============'
        print 'break point: ', item['time'], item['bonus_rate']
        buy_in = 1
        for i in xrange(0, silence_time):
            if index < silence_time:
                buy_in = 0
                print 'unuse point: no enough history'
                break
            if rmb[index -i -1]['time'] != (item['time'] - timedelta(minutes=i+1)):
                buy_in = 0
                print 'unuse point: time not match', rmb[index -i]['time'], item['time'] - timedelta(minutes=i+1)
                break
            if abs(rmb[index -i -1]['bonus_rate']) > stable_rate:
                buy_in = 0
                print 'unuse point: no enough silence', rmb[index -i -1]['bonus_rate']
                break
        if buy_in:
            print 'buyin point: ', item['time'], item
    index = index + 1





















