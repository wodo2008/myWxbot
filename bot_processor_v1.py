#!-*-coding:utf-8-*-

import json
import threading
import time
import redis
from contents import replyMsg
from processor.send_kecheng import send_kecheng
from wxbot import *

reload(sys)
sys.setdefaultencoding('utf8')
#
def init_redis(host,port,db,password=None):
    if password :
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db),password=password)
    else:
        pool = redis.ConnectionPool(host=host,port=int(port),db=int(db))
    return redis.Redis(connection_pool=pool)

class MyWXBot(WXBot):

    def __init__(self):
        WXBot.__init__(self)
        self.send_kecheng = send_kecheng()

    def handle_msg_all(self, msg):
        #消息处理分发
        self.msg_dispather(msg)

    def schedule(self):
        t3 = threading.Thread(target=self.send_msg_to_group_schedule,args=('可测试性设计理论和实践-DFT',))
        t3.start()


    def msg_dispather(self,msg):

        self.group_newer_response(self,'可测试性设计理论和实践-DFT',msg,'')

        msg_type_id = msg['msg_type_id']
        content_type = msg['content']['type']
        if content_type in [3] and 'detail' in msg['content']:
            del msg['content']['detail']
        print 'msg:',msg
        if msg_type_id in [37]:
            self.auto_add_friend(msg)
        elif msg_type_id in [4]:
            self.friend_process(msg)
        #接收群图片
        elif msg_type_id in [3] and content_type in [3]:
            self.group_process(msg)

    def friend_process(self,msg):
        config = self.get_setting_config()
        friend_text_reply = config['friend_text_reply']
        user_id = msg['user']['id']
        keyword = msg['content']['data']
        texts = None
        imgs = None
        group_names = None
        #处理自动回复
        if keyword in friend_text_reply:
            contents = friend_text_reply[keyword]
            texts = contents['texts']
            imgs = contents['imgs']
            group_names = contents['group_names']
        self.send_msg_to_friend(user_id,texts,imgs,group_names)
        #处理后台数据
        self.friend_process_backend(msg)

    def friend_process_backend(self,msg):
        reply_to_sender, reply_to_group = self.send_kecheng.friend_process_backend(msg,self.get_setting_config())
        if 'user_id' in reply_to_sender:
            user_id = reply_to_sender['user_id']
            texts = reply_to_sender.get('texts',None)
            imgs = reply_to_sender.get('imgs',None)
            groups = reply_to_sender.get('groups',None)
            self.send_msg_to_friend(user_id,texts,imgs,groups)
        if 'group_id' in reply_to_group:
            group_id = reply_to_group['group_id']
            texts = reply_to_group.get('texts',None)
            imgs = reply_to_group.get('imgs',None)
            groups = reply_to_group.get('groups',None)
            self.send_msg_to_group(group_id,texts,imgs,groups)

    def group_process(self,msg):
        config = self.get_setting_config()
        group_alias_dict = config['group_alias']
        group_reply = config['group_reply']
        if msg['user']['name'] == 'self':
            ori_group_id = msg['to_user_id']
        else:
            ori_group_id = msg['user']['id']
        sender_id = msg['content']['user']['id']
        group_alias = None
        for k,v in group_alias_dict.items():
            for vi in v:
                if ori_group_id == self.getGroupId(vi):
                    group_alias = k
        reply_to_group = None
        reply_to_sender = None
        content_type = 'img'
        if group_alias and group_alias in group_reply:
            reply_to_sender = group_reply[group_alias][content_type]['reply_to_sender']
            reply_to_group = group_reply[group_alias][content_type]['reply_to_group']
        if reply_to_group:
            texts = reply_to_group['texts']
            imgs = reply_to_group['imgs']
            group_names = reply_to_group['group_names']
            self.send_msg_to_group(ori_group_id,texts,imgs,group_names)
        if reply_to_sender:
            texts = reply_to_sender['texts']
            imgs = reply_to_sender['imgs']
            group_names = reply_to_sender['group_names']
            self.send_msg_to_friend(sender_id, texts, imgs, group_names)
        #处理后台数据
        self.group_process_backend(msg)

    def group_process_backend(self,msg):
        reply_to_sender, reply_to_group = self.send_kecheng.group_process_backend(msg,self.get_setting_config())
        if 'user_id' in reply_to_sender:
            user_id = reply_to_sender['user_id']
            texts = reply_to_sender.get('texts',None)
            imgs = reply_to_sender.get('imgs',None)
            groups = reply_to_sender.get('groups',None)
            self.send_msg_to_friend(user_id,texts,imgs,groups)
        if 'group_id' in reply_to_group:
            group_id = reply_to_group['group_id']
            texts = reply_to_group.get('texts',None)
            imgs = reply_to_group.get('imgs',None)
            groups = reply_to_group.get('groups',None)
            self.send_msg_to_friend(user_id,texts,imgs,groups)
        self.send_msg_to_group(group_id,texts,imgs,groups)


    def send_msg_to_group(self,group_id,texts,imgs,groups):
        if not group_id:
            print 'send_msg_to_friend:no user_id'
            return
        texts = [] if not texts else texts
        imgs = [] if not imgs else imgs
        groups = [] if not groups else groups
        if not isinstance(texts,list):
            texts = [texts]
        if not isinstance(imgs,list):
            imgs = [imgs]
        if not isinstance(groups,list):
            groups = [groups]
        print 'texts:',texts
        print 'imgs:',imgs
        print 'groups:',groups
        for text in texts:
            self.send_msg_by_uid(text, group_id)
        for img in imgs:
            self.send_img_msg_by_uid(img, group_id)
        for group in groups:
            self.self.add_friend_to_group(group_id,group)

    def send_msg_to_friend(self,user_id,texts,imgs,groups):
        if not user_id:
            print 'send_msg_to_friend:no user_id'
            return
        texts = [] if not texts else texts
        imgs = [] if not imgs else imgs
        groups = [] if not groups else groups
        if not isinstance(texts,list):
            texts = [texts]
        if not isinstance(imgs,list):
            imgs = [imgs]
        if not isinstance(groups,list):
            groups = [groups]
        print 'texts:',texts
        print 'imgs:',imgs
        print 'groups:',groups
        for text in texts:
            self.send_msg_by_uid(text, user_id)
        for img in imgs:
            self.send_img_msg_by_uid(img, user_id)
        for group in groups:
            self.add_friend_to_group(user_id,group)

    def get_setting_config(self):
        if (not self.config) or self.need_reload():
            f_path = os.path.dirname(os.path.abspath(__file__))
            conf_path = os.path.join(f_path,'config/config_setting.json')
            self.config = json.load(open(conf_path))
            self.config_has_reload()
        return self.config

    def need_reload(self):
        if not self.redis:
            self.redis = init_redis('127.0.0.1',6379,1)
        if self.redis.exists('mywxbot_config_reload'):
            return False
        return True

    def config_has_reload(self):
        if not self.redis:
            self.redis = init_redis('127.0.0.1',6379,1)
        self.redis.set('mywxbot_config_reload',1,3600 * 12)

    def auto_add_friend(self,msg):
        print 'auto_add_friend'
        self.apply_useradd_requests(msg['content']['data'])

    def getGroupId(self, NickName):
        if NickName in self.groupId_dict and len(self.groupId_dict[NickName]) > 0:
            return self.groupId_dict[NickName]
        groupId = ''
        print os.path.join(os.path.split(os.path.abspath(__file__))[0], 'temp/group_list.json')
        group_list = json.load(open(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'temp/group_list.json')))
        # print 'group_list:',group_list
        for group in group_list:
            # print 'group:',group
            TNickName = group['NickName']
            UserName = group['UserName']
            if TNickName == NickName:
                groupId = UserName
                break
        print NickName, 'is:', groupId
        self.groupId_dict[NickName] = groupId
        return groupId

########################################################
    #定时向群发通知
    def send_msg_to_group_schedule(self,groupname):
        groupId = self.getGroupId(groupname)
        send_msg = replyMsg['group_welWord']
        while True:
            print 'has newer:',self.has_newer
            if self.has_newer:
                textArr = replyMsg['auto_txt']
                imgArr = replyMsg['auto_msg']
                for t in textArr:
                    self.send_msg_by_uid(t, groupId)
                for img in imgArr:
                    self.send_img_msg_by_uid(img, groupId)
                # self.send_msg_by_uid(send_msg, groupId)
                self.has_newer = False
            time.sleep(2 * 60)
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
            self.newerList.append(eval(result[0][1]))



    '''

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
            if len(result) <= 0:
                return
            self.has_newer = True
            self.newerList.append(eval(result[0][1]))

    
    
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
            self.send_msg_by_uid(ret, ori_group_id)


    #自动同意好友请求并发信息
    def auto_add_member_sendMsg(self,qunName,msg):
        print 'auto_add_member_sendMsg:',msg
        if msg['msg_type_id'] in [37]:
            self.apply_useradd_requests(msg['content']['data'])
            user_id = msg['content']['data']['UserName']
            textArr = [replyMsg['auto_add']]
            if not self.auauto_rep:
                self.auto_rep = Auto_replyer()
            # retData = self.auto_rep.replyByMsg(msg)
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
        send_msg = replyMsg['group_welWord']
        while True:
            print 'has newer:',self.has_newer
            if self.has_newer:
                textArr = replyMsg['auto_txt']
                imgArr = replyMsg['auto_msg']
                for t in textArr:
                    self.send_msg_by_uid(t, groupId)
                for img in imgArr:
                    self.send_img_msg_by_uid(img, groupId)
                # self.send_msg_by_uid(send_msg, groupId)
                self.has_newer = False
            time.sleep(2 * 60)

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
            self.redis = set()
            return self.redis
        else:
            return self.redis
    '''


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
