#!-*-coding:utf-*-
'''
用于小程序自动转发问题中，获取
'''

import sqlite3

class QaProcessor(object):
    def __init__(self):
        dburl = '/home/app/fuxinxueba/db.sqlite3'
        self.conn = sqlite3.Connection(dburl)

    def get_unsovler(self):
        cursor = self.conn.cursor()
        sql = 'select grad_weixin_id from qaProgram_question where status = 0'
        datas = cursor.execute(sql)
        weixin_id_set = set()
        for row in datas:
            weixin_id = row[0]
            weixin_id_set.add(weixin_id)
        return weixin_id_set


if __name__ == '__main__':
    qaprocess = QaProcessor()
    widSet = qaprocess.get_unsovler()
    print widSet
