#!/bin/bash
# DATE=$(date +%Y%m%d%H)
begin_time=20150101;
suffix_start=000000;
suffix_end=235959;
suffix_days=days
for i in $(seq 0 1500)
do
    sleep 1;
    # period=`expr $i + $begin_time`;
    # echo $bigin_time+$i$suffix_days
    # echo date
    period=$(date +%Y%m%d -d $bigin_time-$i$suffix_days)
    echo $period
    period_start=$period$suffix_start;
    period_end=$period$suffix_end;
    echo $period_start
    echo $period_end
    sh request.sh $period_start $period_end >> foreign_exchange_history.txt
    # sh request.sh $period_start $period_end #  >> date +%Y%m_history.txt
done
