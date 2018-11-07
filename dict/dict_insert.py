# -*- coding:utf-8 -*-

'''
将dict插入数据库
'''
import re
import pymysql
f = open('dict.txt')
db = pymysql.connect("127.0.0.1 ",'root','123456','dict')
cursor = db.cursor()
for line in f:
    try:
        obj = re.match("([-a-zA-Z]+)\s+(.*)",line)
        word = obj.group(1)
        interpret = obj.group(2)
    except:
        continue
    sql = "insert into words (word,interpret) values ('%s','%s')"%(word,interpret)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        continue
f.close()