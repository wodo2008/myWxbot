#!-*-coding:utf-8-*-

import pymongo

class database_layer(object):
    def __init__(self,project_name):
        conf = {
            "mongo":{"host":"mongodb://127.0.0.1:27017"}
        }
        mongo_host = conf['mongo']['host']
        mongo_conn = pymongo.MongoClient(mongo_host)
        self.table = mongo_conn['eke'][project_name]

    def get_by_userid(self,userid):
        print 'database_layer:get_by_userid'
        query = {'user_id':userid}
        return self.table.find_one(query)

    def save(self,item):
        print 'database_layer:save'
        self.table.save(item)
