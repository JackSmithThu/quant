#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from pytz import timezone

cn_tz = timezone('Asia/Shanghai')
us_tz = timezone('America/Chicago')

f = open('tmp_history.txt','r')
for line in f.readlines():
    try:
        # print line,
        words = line.split(',')
        if len(words) < 2:
            continue
        [date_string, data] = line.split(',',1)
        date_time = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        print 'us time: ' + date_string + ','+ data,
        us_date_time = us_tz.localize(date_time)
        cn_date_time = us_date_time.astimezone(cn_tz)
        cn_date_time_string = cn_date_time.strftime('%Y-%m-%d %H:%M')
        print 'cn_time: '+ cn_date_time_string + ',' + data,
        print '===================='
    except Exception:
        print 'some thing wrong happend!', Exception.message
        continue
f.close()
