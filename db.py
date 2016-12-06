#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
host="localhost"
user="ewg"
passwd="ewg_123456"
db="ewg"
# 打开数据库连接

def get_db():
    conn = MySQLdb.connect(host,user,passwd,db)
    return conn

conn = get_db()
cur = conn.cursor()
cur.execute("select * from category limit 10")
print cur.fetchone()