#!/bin/bash

source /etc/profile;
source ~/.bash_profile;

cd /home/myWxbot
DATE=$(date +'%Y-%m-%d %H:%M')
echo $DATE

ps -ef|grep send_unsovled_q |grep -v grep|awk  '{print "kill -9 " $2}' |sh

nohup python /home/myWxbot/send_unsovled_q.py &
python /home/myWxbot/send_email.py
rm -rf /home/myWxbot/wxqr_fold/wxqr.png
