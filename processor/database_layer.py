#!-*-coding:utf-8-*-

import pymongo

class Database_layer(object):
    def __init__(self,conf):
        mongo_host = conf['mongo']['host']
        mongo_conn = pymongo.MongoClient(mongo_host)
        self.user_identi_code = mongo_conn.eke.user_identi_code
        self.user_res_process = mongo_conn.eke.user_res_process
        pass

    def get_uic_Item(self,query):
        return self.user_identi_code.find_one(query)

    def save_uic_Item(self,item):
        self.user_identi_code.save(item)

    def get_urp_Item(self,query):
        return self.user_res_process.find_one(query)

    def save_urp_Item(self,item):
        self.user_res_process.save(item)