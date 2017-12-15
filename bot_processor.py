#!-*-coding:utf-8-*-
#

from wxbot import *
# import redis
import time
from datastatis_ploty import line_plot
import json
import threading
from processor.database_layer import Database_layer
# import redis
from processor.qaProcessor import QaProcessor
from processor.auto_replyer_v2 import Auto_replyer
import contents

reload(sys)
sys.setdefaultencoding('utf8')

# def init_redis(host,port,db,password=None):
#     if password :
#         pool = redis.ConnectionPool(host=host,port=int(port),db=int(db),password=password)
#     else:
#         pool = redis.ConnectionPool(host=host,port=int(port),db=int(db))
#     return redis.Redis(connection_pool=pool)

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        print 'msg:',msg
        self.send_kecheng_v2(msg,'IC交流群3|打同学吧')

        #self.get_fixFriendMsg('大同学吧小助手',msg)
        # if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
        #     print msg['user']['id']
        #     #self.send_msg_by_uid(u'hi', msg['user']['id'])
        #     print msg['user']['id']
        #     self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

    def schedule(self):
        # t1 = threading.Thread(target=self.stats_plot,args=('ceshi',))
        # t1 = threading.Thread(target=self.stats_plot,args={'卓工生涯工作室交流群'})
        # t1.start()
        # t2 = threading.Thread(target=self.send_unsovled_q,args={})
        # t2.start()
        t3 = threading.Thread(target=self.send_msg_to_group,args=('IC交流群3|打同学吧',))
        t3.start()

    def send_kecheng_v2(self,msg,qunName):
        self.group_newer_response(qunName, msg,'')
        self.get_send_img_members(qunName, msg)
        self.auto_add_member_sendMsg(qunName,msg)
        self.reply_to_friends(qunName,msg)


    def get_fixFriendMsg(self,friend,msg):
        fromFriend = msg.get('user',{}).get('name','')
        if friend == fromFriend:
            self.paramDict['qunName'] = msg.get('content',{}).get('data','')

    #对于新加入的进行回应
    def group_newer_response(self,g_pinyin,msg,welWord):
        print 'group_newer_response'
        if msg['user']['name'] == 'self':
            ori_group_id = msg['to_user_id']
        else:
            ori_group_id = msg['user']['id']
        print 'g_pinyin:',g_pinyin
        print self.getGroupId(g_pinyin),ori_group_id
        if not ori_group_id == self.getGroupId(g_pinyin):
            print 'need:%s,this is %s' % (self.getGroupId(g_pinyin),ori_group_id)
            return
        #群文本信息
        group_invit_1 = re.compile(u'(.*?)邀请(.*?)加入了群聊')
        group_invit_2 = re.compile(u'(.*?)通过扫描(.*?)分享的二维码加入群聊')
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 12:
            result1 = group_invit_1.findall(msg['content']['data'])
            result2 = group_invit_2.findall(msg['content']['data'])
            result = result1 if len(result1) > 0 else result2
            #print result1,result2,result
            if len(result) <= 0:
                return
            # send_msg = '@%s,%s' % (eval(result[0][1]),welWord)
            #self.send_msg_by_uid(send_msg,msg['user']['id'])
            self.has_newer = True

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
            if not self.auauto_rep:
                self.auto_rep = Auto_replyer()
            ret = self.auto_rep.img_process(msg)
            self.send_msg_by_uid(ret, msg['user']['id'])

    #好友信息处理
    def reply_to_friends(self,qunName,msg):
        user_id = msg['user']['id']
        if not self.auauto_rep:
            self.auto_rep = Auto_replyer()
        retData = self.auto_rep.replyByMsg(msg)
        if isinstance(retData,str):
            self.send_msg_by_uid(retData, user_id)
        if isinstance(retData,dict):
            textArr = retData['text']
            imgArr = retData['img']
            for t in textArr:
                self.send_msg_by_uid(t, user_id)
            for img in imgArr:
                self.send_img_msg_by_uid(img, user_id)
            print 'qunName:',qunName
            self.add_friend_to_group(user_id, qunName)

    #自动同意好友请求并发信息
    def auto_add_member_sendMsg(self,qunName,msg):
        if msg['msg_type_id'] == 37:
            self.apply_useradd_requests(msg['content']['data'])
            user_id = msg['content']['data']['UserName']
            textArr = [contents.replyMsg['auto_add']]
            if not self.auauto_rep:
                self.auto_rep = Auto_replyer()
            retData = self.auto_rep.newerAdd(msg)
            for t in textArr:
                 self.send_msg_by_uid(t,user_id)
            print 'qunName:',qunName
            self.add_friend_to_group(user_id,qunName)


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
                if NickName in ['Jason L']:
                    continue
                if NickName not in has_Img_users:
                    print u'%s NO IMG，REMOVE!' % NickName
                    self.delete_user_from_group(NickName,gid)
            time.sleep(100)

    #定时向群发通知
    def send_msg_to_group(self,groupname):
        groupId = self.getGroupId(groupname)
        send_msg = contents.replyMsg['group_welWord']
        while True:
            print 'has newer:',self.has_newer
            if self.has_newer:
                self.send_msg_by_uid(send_msg, groupId)
                self.has_newer = False
            time.sleep(60)

    def getGroupId(self,NickName):
        if NickName in self.groupId_dict and len(self.groupId_dict[NickName])>0:
            return self.groupId_dict[NickName]
        groupId = ''
        print os.path.join(os.path.split(os.path.abspath(__file__))[0],'temp\group_list.json')
        group_list = json.load(open(os.path.join(os.path.split(os.path.abspath(__file__))[0],'temp\group_list.json')))
        # print 'group_list:',group_list
        for group in group_list:
            # print 'group:',group
            TNickName= group['NickName']
            UserName = group['UserName']
            if TNickName == NickName:
                groupId = UserName
                break
        print NickName,'is:',groupId
        self.groupId_dict[NickName] = groupId
        return groupId

    def stats_plot(self,qunPinyin):
        print 'Start Stats_plot'
        groupId = self.getGroupId(qunPinyin)
        print 'groupId:',groupId
        while True:
            if is_send([8]):
                print 'stats_plot process'
                line_plot(10000)
                #self.send_img_msg_by_uid('data_statis.png',self.get_user_id('Tobe_Lu'))
                self.send_img_msg_by_uid('data_statis.png',self.get_user_id('wodo2008'))
                self.send_img_msg_by_uid("data_statis.png", groupId)
            time.sleep(3600)

    def send_unsovled_q(self):
        qaproces = QaProcessor()
        while True:
            if not is_send([9,20]):
                time.sleep(3600)
                return
            toUserSet = set()
            qrPath = 'grad_qrs/%s.jpg'
            now = time.time()
            nowstr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))
            msgtext = '亲，截至%s,您在大同学吧还有如下问题没有回答，请在近期给予答复~' % nowstr
            toUserSet = qaproces.get_unsovler()
            print 'toUserSet:',toUserSet
            for user in toUserSet:
                print 'send user:',user,qrPath % user
                if not os.path.exists(qrPath % user):
                    continue
                self.send_msg(user,msgtext)
                self.send_img_msg_by_uid(qrPath % user,self.get_user_id(user))
                self.send_msg(u'wodo2008','%s:%s' % (user,msgtext))
                self.send_img_msg_by_uid(qrPath % user,self.get_user_id(u'wodo2008'))
            time.sleep(3600)

    def getRedis(self):
        if self.redis == None:
            # self.redis = init_redis('127.0.0.1', 6379, 0)
            self.redis = set()
            return self.redis
        else:
            return self.redis


def is_send(hourArr):
    if not isinstance(hourArr,list):
        return False
    now = time.time()
    hour = int(time.strftime('%H',time.localtime(now)))
    if hour in hourArr:
        return True
    return False

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
    #测试git
