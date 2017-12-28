#！-*-coding:utf-8-*-

import os
from database_layer import database_layer

class send_kecheng(object):
    def __init__(self):
        project_name = 'send_kecheng_v2'
        self.dl = database_layer(project_name)

    def group_process_backend(self,msg,config):
        msg_type_id = msg['msg_type_id']
        content_type = msg['content']['type']
        reply_to_group = {}
        reply_to_sender = {}
        if msg_type_id in [3] and content_type in [3]:
            user_id = msg['content']['user']['id']
            if msg['user']['name'] == 'self':
                ori_group_id = msg['to_user_id']
            else:
                ori_group_id = msg['user']['id']
            status = self.group_img_process(user_id)
            if status == 'both_has':
                reply_to_group['text'] = config['group_process_backend']['reply_to_group']['both_has']
                reply_to_group['group_id'] = ori_group_id
                reply_to_sender['text'] = config['group_process_backend']['reply_to_sender']['both_has']
                reply_to_sender['user_id'] = user_id
            elif status == 'no_phone':
                reply_to_group['text'] = config['group_process_backend']['reply_to_group']['no_phone']
                reply_to_group['group_id'] = ori_group_id
                reply_to_sender['text'] = config['group_process_backend']['reply_to_sender']['no_phone']
                reply_to_sender['user_id'] = user_id
        print 'reply_to_sender:',reply_to_sender
        print 'reply_to_group:',reply_to_group
        return reply_to_sender, reply_to_group


    def friend_process_backend(self,msg,config):
        msg_type_id = msg['msg_type_id']
        user_id = msg['user']['id']
        reply_to_group = {}
        reply_to_sender = {}
        if msg_type_id in [4]:
            rev_data = msg['content']['data']
            if len(rev_data) == 11 and rev_data.isdigit():
                status = self.friend_phone_process(user_id,rev_data)
                if status == 'both_has':
                    reply_to_sender['text'] = config['friend_process_backend']['reply_to_sender']['both_has']
                    reply_to_sender['user_id'] = user_id
                elif status == 'no_img':
                    reply_to_sender['text'] = config['friend_process_backend']['reply_to_sender']['no_img']
                    reply_to_sender['user_id'] = user_id
        print 'reply_to_sender:',reply_to_sender
        print 'reply_to_group:',reply_to_group
        return reply_to_sender, reply_to_group


    def group_img_process(self, user_id):
        query = {'user_id':user_id}
        data = self.dl.get_by_query(query)
        if not data:
            data = {}
            data['user_id'] = user_id
        data['hasImg'] = True
        self.dl.save(data)
        if 'phoneNum' in data:
            status = 'both_has'
        else:
            status = 'no_phone'
        return status


    def friend_phone_process(self,user_id,phoneNum):
        query = {'user_id':user_id}
        data = self.dl.get_by_query(query)
        if not data:
            data = {}
            data['user_id'] = user_id
        data['phoneNum'] = phoneNum
        self.dl.save(data)
        if 'hasImg' in data and data['hasImg']:
            status = 'both_has'
        else:
            status = 'no_img'
        return status