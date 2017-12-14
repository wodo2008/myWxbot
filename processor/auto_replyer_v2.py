#!-*-coding:utf-8-*-

from database_layer import Database_layer
from AutoReplyDict import StageDict
import time
import json

class Auto_replyer(object):
    def __init__(self):
        conf = {
            "mongo":{"host":"mongodb://127.0.0.1:27017"}
        }
        self.dl = Database_layer(conf)
        self.urpItem = None

    #根据接收的消息返回对应的消息
    def replyByMsg(self,msg):
        data = msg['content']['data']
        userId = msg['user']['id']
        query = {'userId': userId}
        urpItem = self.dl.get_urp_Item(query)
        stage = urpItem['stage']
        if stage == StageDict['registed']:
            print 'registed'
            return ''
        if len(data) == 11 and data.isdigit():
            print 'phone_process'
            return self.phone_process(data, urpItem)
        else:
            print 'send_correct_phoneNumReq'
            return self.send_correct_phoneNumReq()

    def get_send_img_members(self, qunPinyin, msg):
        if msg['user']['name'] == 'self':
            ori_group_id = msg['to_user_id']
        else:
            ori_group_id = msg['user']['id']
        if not ori_group_id == self.getGroupId(qunPinyin):
            print 'need:%s,this is %s' % (self.getGroupId(qunPinyin), ori_group_id)
            return
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 3:
            name = msg['content']['user']['name']
            print '%s has send Img' % name
            query = {'userId': name}
            urpItem = self.dl.get_urp_Item(query)
            if not urpItem:
                urpItem = {}
            



    #处理图片
    def img_process(self,msg,urpItem):
        urpItem['stage'] = StageDict['hasImg']
        self.dl.save_urp_Item(urpItem)
        return self.send_ask_phoneNum()

    #处理文字
    def text_process(self,msg):
        text = msg['content']['data']
        pass

    #处理电话号码
    def phone_process(self,phone,urpItem):
        query = {'phoneNum':phone}
        uicItem = self.dl.get_uic_Item(query)
        if not uicItem:
            return self.send_wrong_phone()
        uicItem['hasRight'] = True
        self.dl.save_uic_Item(uicItem)
        urpItem['stage'] = StageDict['registed']
        self.dl.save_urp_Item(urpItem)
        return self.send_success_regist()


    def send_kecheng(self,userId):
        query = {'userId': userId}
        urp = self.dl.get_urp_Item(query)
        if not urp:
            urp = {}
            urp['userId'] = userId
            urp['timeStmp'] = time.time()
            urp['stage'] = StageDict['welcome']
            self.dl.save_urp_Item(urp)
        data = json.load(open('/home/myWxbot/config.json'))
        textArr = data['auto_txt']
        imgArr = data['auto_msg']
        retData = {}
        retData['text'] = textArr
        retData['img'] = imgArr
        return retData


    #到群提问的信息
    def send_ask_fromGroup(self):
        str = '您好，由于当前小助手好友过多，如有疑惑请前往【IC交流群2|大同学吧】中进行提问，非常感谢！[太阳]'
        return str

    def send_ask_phoneNum(self):
        str = '截图已收到！请回复您之前报名的手机号，我们将为该账号开通课程特权[嘿哈]【注意：回复内容需要为纯数字】'
        return str

    def send_correct_phoneNumReq(self):
        str = '不好意思，您的号码输入格式有误，只要纯数字就好啦[呲牙]'
        return str

    def send_wrong_phone(self):
        str = '呃，似乎出了点问题…您刚刚回复的号码并未报名本次活动。不过没关系，点此链接立即报名：www.fuxinxueba.com/userpa/index'
        return str

    def send_success_regist(self):
        str = '号码审核通过，明天中午12点后，您可以登陆E课网观看此课程【新用户账号和密码均为手机号。老用户用户名为手机号，密码不变】！感谢您对于本活动的大力支持，下次活动我们再见[奸笑]'
        return str

