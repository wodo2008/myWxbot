#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
# import redis
import time
from datastatis_ploty import line_plot
import json
import threading
import redis

def init_redis(host,port,db,password=None):
    if password :
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db),password=password)
    else:
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db))
    return redis.Redis(connection_pool=pool)

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        #print msg['user']['id']
        self.group_newer_response(u'ceshi',msg)
        self.get_send_img_members(u'ceshi',msg)
        self.auto_add_member(msg)
        # if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
        #     print msg['user']['id']
        #     #self.send_msg_by_uid(u'hi', msg['user']['id'])
        #     print msg['user']['id']
        #     self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

    def schedule(self):
        # t1 = threading.Thread(target=self.stats_plot,args=('ceshi',))
        t1 = threading.Thread(target=self.stats_plot,args={'zhuogongshengyagongzuoshijiaoliuqun'})
        t1.start()
        # t2 = threading.Thread(target=self.remove_members_fromGroup,args=('ceshi',))
        # t2.start()

    #对于新加入的进行回应
    def group_newer_response(self,g_pinyin,msg):
        print msg
        if msg['user']['name'] == 'self':
            ori_group_id = msg['to_user_id']
        else:
            ori_group_id = msg['user']['id']
        if not ori_group_id == self.getGroupId(g_pinyin):
            print 'need:%s,this is %s' % (self.getGroupId(g_pinyin),ori_group_id)
            return
        #群文本信息
        group_invit_1 = re.compile(u'(.*?)邀请(.*?)加入了群聊')
        group_invit_2 = re.compile(u'(.*?)通过扫描(.*?)分享的二维码加入群聊')
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            result1 = group_invit_1.findall(msg['content']['data'])
            result2 = group_invit_2.findall(msg['content']['data'])
            result = result1 if len(result1) > 0 else result2
            if len(result) <= 0:
                return
            send_msg = '@%s欢迎加入' % (result[0][1])
            self.send_msg_by_uid(send_msg,msg['user']['id'])

    #获取发送图片的成员
    def get_send_img_members(self,qunPinyin,msg):
        if msg['user']['name'] == 'self':
            ori_group_id = msg['to_user_id']
        else:
            ori_group_id = msg['user']['id']
        if not ori_group_id == self.getGroupId(qunPinyin):
            print 'need:%s,this is %s' % (self.getGroupId(qunPinyin),ori_group_id)
            return
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 3:
            name = msg['content']['user']['name']
            print '%s has send Img' % name
            tRedis = self.getRedis()
            #tRedis.sadd('hasImgUsers',user_id)
            tRedis.add(name)
    #自动同意好友请求
    def auto_add_member(self,msg):
        if msg['msg_type_id'] == 37:
            self.apply_useradd_requests(msg['content']['data'])
            user_id = msg['content']['data']['UserName']
            self.send_msg_by_uid(u"欢迎",user_id)
            self.add_friend_to_group(user_id,u'IC交流群|大同学吧')


    #从群中移除指定的成员
    def remove_members_fromGroup(self,qunPinyin):
        print 'remove_members_fromGroup Process...'
        while True:
            tRedis = self.getRedis()
            #has_Img_users = tRedis.smembers('hasImgUsers')
            has_Img_users = tRedis
            gid = self.getGroupId(qunPinyin)
            all_group_members = json.load(open(os.path.join(os.path.split(os.path.abspath(__file__))[0],'temp/group_users.json')))
            group_members = all_group_members[gid]
            for gm in group_members:
                NickName = gm['NickName']
                if NickName in [u'Jason L']:
                    continue
                if NickName not in has_Img_users:
                    print u'%s NO IMG，REMOVE!' % NickName
                    self.delete_user_from_group(NickName,gid)
            time.sleep(100)

    def getGroupId(self,qunPinyin):
        if qunPinyin in self.groupId_dict:
            return self.groupId_dict[qunPinyin]
        groupId = ''
        print os.path.join(os.path.split(os.path.abspath(__file__))[0],'temp/group_list.json')
        group_list = json.load(open(os.path.join(os.path.split(os.path.abspath(__file__))[0],'temp/group_list.json')))
        for group in group_list:
            print 'group:',group
            PYQuanPin= group['PYQuanPin']
            UserName = group['UserName']
            if PYQuanPin == qunPinyin:
                groupId = UserName
                break
        self.groupId_dict[qunPinyin] = groupId
        return groupId

    def stats_plot(self,qunPinyin):
        print 'Start Stats_plot'
        groupId = self.getGroupId(qunPinyin)
        print 'groupId:',groupId
        canSend = True
        while True:
            print 'stats_plot process'
            if is_send_statsPlot() and canSend:
                line_plot(10000)
                self.send_img_msg_by_uid('data_statis.png',self.get_user_id('Tobe_Lu'))
                self.send_img_msg_by_uid('data_statis.png',self.get_user_id('wodo2008'))
                self.send_img_msg_by_uid("data_statis.png", groupId)
                canSend = False
            if not is_send_statsPlot():
                canSend = True
            time.sleep(3600)

    def send_unsovled_q(self):
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
            time.sleep(200)
        for user in toUserSet:
            print 'send user:',user,qrPath % user
            self.send_msg(user,msgtext)
            self.send_img_msg_by_uid('data_statis.png',self.get_user_id('Tobe_Lu'))
            self.send_img_msg(user,qrPath % user)
            self.send_msg(u'wodo2008',msgtext)
            self.send_img_msg(u'wodo2008', qrPath % user)
            time.sleep(100)


    def getRedis(self):
        if self.redis == None:
            # self.redis = init_redis('127.0.0.1', 6379, 0)
            self.redis = set()
            return self.redis
        else:
            return self.redis


def is_send_statsPlot():
    now = time.time()
    hour = int(time.strftime('%H',time.localtime(now)))
    if hour == 11:
        return True
    return False
#根据群名称的拼音获取群的ID


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
    #测试git
