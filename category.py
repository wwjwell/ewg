# -*- coding: utf-8 -*-
import json
import urllib
f = open('category.json')
pj = json.load(f)
#{"name":"Blush","url":"/skindeep/browse/blush/"},
#{"name":"Wound treatment","url":"/skindeep/browse/wound+treatment/"}
#{"name":"Acne treatment","url":"/skindeep/browse/acne+treatment/"},
class Category:
	def __init__(self,name,url):
		self.name = name
		self.url = url
		self.category = urllib.quote(url[len('/skindeep/browse/'):len(url)-1].replace('+','_'))
lst = []
for item in pj:
	c = Category(item['name'],item['url'])
	lst.append(c)

def get_categories():
	return lst
