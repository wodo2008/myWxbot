#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import redis

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
            self.send_msg_by_uid(u'hi', msg['user']['id'])
            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])


    def schedule(self):
        #self.send_msg_by_uid(u'hi', userid)
        #ques_grad_str = '%s|%s' % (grad_weixin_id, content)
        mgRedis = init_redis('127.0.0.1', 6379, 0)
        while True:
            msgStr = mgRedis.lpop('ques_grad_mq')
            print msgStr
            if not msgStr:
                time.sleep(5)
                continue
            msgarr = msgStr.split('|')
            if len(msgarr) == 2:
                toUser = msgarr[0]
                msg = msgarr[1]
            self.send_msg(toUser,msg)
            self.send_msg(u'xinba', msg)


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
    #测试git
