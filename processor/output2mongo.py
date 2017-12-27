#!-*-coding:utf-8-*-
import pymongo
import sys
import os

def qaProgram_answer():
    filenamelist = ['qaProgram_answer','qaProgram_graddetail','qaProgram_question']
    columnsdict = {}
    columnsdict['qaProgram_answer']=['aid','content','grad_weixin_id','answer_time','qid']
    columnsdict['qaProgram_graddetail'] = ['gid','name','company','school','specialty','grad_weixin_id','avatar']
    columnsdict['qaProgram_question'] = ['qid','title','content','status','grad_weixin_id','asker_openid','ask_time']
    mongo_conn = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    fname = ''
    for filename in filenamelist:
        table = mongo_conn.qaProgram[filename]
        columns = columnsdict[filename]
        rf = open('%.txt' % filename)
        rlines = rf.readlines()
        for rl in rlines:
            values = rl.split('|')
            data = {}
            for i in range(len(columns)):
                data[columns[i]] = values[i]
            table.save(data)




