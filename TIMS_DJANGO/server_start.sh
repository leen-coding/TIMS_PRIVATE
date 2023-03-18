#!/bin/bash

redis_start=${1:-1}
source ~/anaconda3/bin/activate TIMS

python3 ./LIVE_VIDEO/manage.py runserver 0.0.0.0:8080 &

pid1=$!

python3 ./TIMS_SITE/manage.py runserver 0.0.0.0:8000 &
pid2=$!

if [ $redis_start -eq 1 ]; then
	python ./LIVE_VIDEO/redisdb.py &
	pid3=$!
	echo "redisdb start!"

else

	echo "redisdb disabled!!"
fi

trap "kill $pid1 $pid2 $pid3" SIGINT

wait






