#!-*-coding:utf-8 -*-
import os
import re
if __name__ == '__main__':
    print os.path.abspath(__file__)
    ss = '点点滴滴2333ddd33'
    s = re.findall("\d+",ss)[1]
    print filter(str.isdigit, ss)