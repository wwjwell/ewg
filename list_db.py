#!/usr/bin/python
# -*- coding: UTF-8 -*-
import db
config = {'host': '10.1.21.245',  # 默认127.0.0.1
          'user': 'off_dbim',
          'password': 'WRo23991230',
          'port': 3312,  # 默认即为3306
          'database': 'im',
          'charset': 'utf8'  # 默认即为utf8
          }
mysqlDb = db.MySQLDB(config)
res = mysqlDb.query_rows("select * from black_list limit 10")
print res
