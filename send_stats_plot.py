#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
# import redis
import time
from datastatis_ploty import line_plot
import json

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        #print msg['user']['id']
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            print msg['user']['id']
            #self.send_msg_by_uid(u'hi', msg['user']['id'])
            print msg['user']['id']
            self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

    def schedule(self):
        groupId = getGroupId('zhuogongshengyagongzuoshijiaoliuqun')
        print 'groupId:',groupId
        canSend = True
        while True:
            if is_send_statsPlot() and canSend:
                line_plot(10000)
                #self.send_img_msg(u'Tobe_Lu', 'data_statis.png')
                self.send_img_msg(u'wodo2008', 'data_statis.png')
                self.send_img_msg_by_uid("data_statis.png", groupId)
                self.send_img_msg(groupId, 'data_statis.png')
                canSend = False
            if not is_send_statsPlot():
                canSend = True
            time.sleep(100)

def is_send_statsPlot():
    now = time.time()
    hour = int(time.strftime('%H',time.localtime(now)))
    if hour == 11:
        return True
    return False

def getGroupId(pinyin):
    groupId = ''
    print os.path.join(os.path.split(os.path.abspath(__file__))[0],'tmp\\group_list.json')
    group_list = json.load(open(os.path.join(os.path.split(os.path.abspath(__file__))[0],'tmp\\group_list.json')))
    for group in group_list:
        PYQuanPin= group['PYQuanPin']
        UserName = group['UserName']
        if PYQuanPin == pinyin:
            groupId = UserName
            break
    return groupId


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
    #测试git
