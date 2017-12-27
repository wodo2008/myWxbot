#!/usr/bin/env python
# coding: utf-8
#

# import redis
import time

import redis
from script.wxbot1 import *

from processor.datastatis_ploty import line_plot


def init_redis(host,port,db,password=None):
    if password :
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db),password=password)
    else:
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db))
    return redis.Redis(connection_pool=pool)

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        print msg['user']['id']
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            print msg['user']['id']
            #self.send_msg_by_uid(u'hi', msg['user']['id'])
            print msg['user']['id']
            self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])


    def schedule(self):
        #self.send_msg_by_uid(u'hi', userid)
        #ques_grad_str = '%s|%s' % (grad_weixin_id, content)
        # mgRedis = init_redis('127.0.0.1', 6379, 0)
        toUserSet = set()
        qrPath = 'grad_qrs/%s.jpg'
        now = time.time()
        nowstr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))
        msgtext = '亲，截至%s,您在大同学吧还有如下问题没有回答，请在近期给予答复~' % nowstr

        while True:
        #     msgStr = mgRedis.lpop('ques_grad_mq')
        #     print msgStr
        #     if not msgStr:
        #         #time.sleep(5)
        #         break
        #     msgarr = msgStr.split('|')
        #     if len(msgarr) == 2:
        #         toUser = msgarr[0]
        #         msg = msgarr[1]
        #         toUserSet.add(toUser)
        #     self.send_img_msg(u'wodo2008','data_statis.png')
        #     time.sleep(200)
        # for user in toUserSet:
        #     print 'send user:',user,qrPath % user
        #     self.send_msg(user,msgtext)
        #     self.send_img_msg(user,qrPath % user)
        #     self.send_msg(u'wodo2008',msgtext)
        #     self.send_img_msg(u'wodo2008', qrPath % user)
            line_plot(10000)
            self.send_img_msg(u'Tobe_Lu', 'data_statis.png')
            self.send_img_msg_by_uid("data_statis.png", u'@@7526ebd681338fa665b7ad0d7cff91b70aab910658ab3462aa587d79e6740121')
            self.send_msg_by_uid('hello',u'@@7526ebd681338fa665b7ad0d7cff91b70aab910658ab3462aa587d79e6740121')
            time.sleep(1000)



def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
    #测试git
