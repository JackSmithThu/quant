#!/bin/bash
# DATE=$(date +%Y%m%d%H)
begin_time=20150101;
suffix_hours=hours;
time_diff=1;
for i in $(seq 0 1500)
do
    sleep 1;
    period_start=$(date +%Y%m%d%H%M%S -d -$time_diff$suffix_hours)
    period_end=$(date +%Y%m%d%H%M%S)
    echo $period_start
    echo $period_end
    # sh history_request.sh $period_start $period_end >> foreign_exchange_realtime.txt
    sh request.sh $period_start $period_end #  >> date +%Y%m_history.txt
done
