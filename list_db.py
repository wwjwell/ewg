#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import json
 
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='ewg',
        passwd='ewg_123456',
        db ='ewg',
        charset="UTF8"
        )

class Goods:
	def __init__(self):
		self.id = '' 
		self.rowId = ''
		self.name = ''
		self.category = ''
		self.href = ''
		self.imgUrl = ''
		self.desc = ''
		self.score = ''
		self.concerns = []
		self.ingredients = []
class Concern:
	def __init__(self,id,field,score):
		self.id = id
		self.field = field
		self.score = score
class Ingredient:
	def __init__(self,id,name):
		self.id = id
		self.name = name

def read_detail():
	
	f = open('detail_json.txt','r')
	idx = 1
	g_lst = []
	c_lst = []
	i_lst = []
	for line in f.readlines():
		print "line=",idx
		idx += 1
		if len(g_lst) > 100:
			insert(g_lst,c_lst,i_lst)
			g_lst = []
			c_lst = []
			i_lst = []

		detail = json.loads(line)
		g = Goods()
		g.id = detail['id'].replace('\'','\\\'')
		g.category = detail['category'].replace('\'','\\\'')
		g.href = detail['href'].replace('\'','\\\'')
		g.name = detail['name'].replace('\'','\\\'')
		g.rowId = detail['rowId'].replace('\'','\\\'')
		g.score = detail['score'].replace('\'','\\\'')
		g.imgUrl = detail['imgUrl'].replace('\'','\\\'')
		g.desc = detail['desc'].replace('\'','\\\'')
		for _i in  detail['ingredients']:
			i_lst.append(Ingredient(g.id,_i))
		for _c in detail['concerns']:
			c_lst.append(Concern(g.id,_c['field'],_c['score']))

		g_lst.append(g)
	
	insert(g_lst,c_lst,i_lst)


def insert(goods_lst=list,concern_lst=list,ingredient_lst=list):
	cur = conn.cursor()
	g_lst=[]
	c_lst=[]
	i_lst=[]
	sql1="insert into goods (id,category,name,href,row_id,score,img_url,description) values ('%s','%s','%s','%s','%s','%s','%s','%s')"
	sql2="insert into goods_concern (id,field,score) values('%s','%s','%s')"
	sql3="insert into goods_ingredient (id,name) values('%s','%s')"

	for g in goods_lst:
		#print g.id,g.category,g.name,g.href,g.rowId,g.score,g.imgUrl,g.desc
		g_lst.append(
			(MySQLdb.escape_string(g.id),
				MySQLdb.escape_string(g.category),
				MySQLdb.escape_string(g.name),
				MySQLdb.escape_string(g.href),
				MySQLdb.escape_string(g.rowId),
				MySQLdb.escape_string(g.score),
				MySQLdb.escape_string(g.imgUrl),
				MySQLdb.escape_string(g.desc)))
	for c in concern_lst:
		c_lst.append(
			(MySQLdb.escape_string(c.id),
				MySQLdb.escape_string(c.field),
				MySQLdb.escape_string(str(c.score))))
	for i in ingredient_lst:
		i_lst.append((MySQLdb.escape_string(i.id),MySQLdb.escape_string(i.name)))
	
	
	cur.executemany(sql1,tuple(g_lst))
	cur.executemany(sql2,c_lst)
	cur.executemany(sql3,i_lst)
	cur.commit()
	cur.close()



if __name__ == '__main__':
	read_detail()