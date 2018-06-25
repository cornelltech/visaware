#!/bin/bash

# clear
# vcgencmd measure_temp
#sysbench --test=cpu --cpu-max-prime=20000 --num-threads=4 run > /dev/null 2>&1

date > temps.out
while true; do
	vcgencmd measure_temp >> temps.out
        sleep 10
done

