#!/bin/bash

source /etc/profile;
source ~/.bash_profile;

cd /home/myWxbot/script
DATE=$(date +'%Y-%m-%d %H:%M')
echo $DATE

ps -ef|grep send_unsovled_q |grep -v grep|awk  '{print "kill -9 " $2}' |sh

python /home/myWxbot/send_unsovled_q.py
python /home/myWxbot/send_email.py
