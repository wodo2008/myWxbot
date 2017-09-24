#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import redis
import time

def init_redis(host,port,db,password=None):
    if password :
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db),password=password)
    else:
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db))
    return redis.Redis(connection_pool=pool)

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):

        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            print msg['user']['id']
            #self.send_msg_by_uid(u'hi', msg['user']['id'])
            print msg['user']['id']
            self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])


    def schedule(self):
        #self.send_msg_by_uid(u'hi', userid)
        #ques_grad_str = '%s|%s' % (grad_weixin_id, content)
        mgRedis = init_redis('127.0.0.1', 6379, 0)
        toUserSet = set()
        qrPath = 'grad_qrs/%s.jpg'
        now = time.time()
        nowstr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))
        msgtext = '亲，截至%s,您在大同学吧还有如下问题没有回答，请在近期给予答复~' % nowstr

        while True:
            msgStr = mgRedis.lpop('ques_grad_mq')
            print msgStr
            if not msgStr:
                #time.sleep(5)
                break
            msgarr = msgStr.split('|')
            if len(msgarr) == 2:
                toUser = msgarr[0]
                msg = msgarr[1]
                toUserSet.add(toUser)
        for user in toUserSet:
            print 'send user:',user,qrPath % user
            self.send_msg(user,msgtext)
            self.send_img_msg(user,qrPath % user)
            self.send_msg(u'wodo2008', msgtext)
            self.send_img_msg(u'wodo2008', qrPath % user)


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
    #测试git
