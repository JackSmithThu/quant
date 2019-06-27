#!/usr/bin/env python
# coding=utf-8

file = open("res.txt")
div = [] # 需要除权的 list，每个元素第一列是时间，第二列是价格（string）

for line in file:
    # print line
    line = line.split('\n')[0]
    div.append(line.split(' '))
    # print div

for div_node in div:
    price = float(div_node[1])
    # print price, type(price)

base_data = open("base.csv")

for line in base_data:
    # print '================'
    # print 'pre:', line,
    line = line.split('\r\n')[0]
    base = line.split(',')
    [year, month, day] = base[0].split('/') 
    month = '0' + month if len(month) < 2 else month
    day = '0' + day if len(day) < 2 else day
    date = year + '-' + month + '-' + day
    arr = []
    for i in xrange(2,6):
        arr.append(float(base[i]))

    for div_item in div:
        if date < div_item[0]:
            # print 'sub:', div_item
            i = 0
            for pri in arr:
                arr[i] = pri - float(div_item[1])
                i = i + 1

    div_pri = []
    for arr_item in arr:
        div_pri.append("%.3f" % arr_item)

    converted = [date+' '+ base[1]] + div_pri + base[6:]
    # print 'res:', ','.join(converted)
    print ','.join(converted)

