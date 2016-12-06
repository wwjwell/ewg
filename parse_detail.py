# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.selector import Selector
import os
import json
import category
class Ingredient:
	def __init__(self,name,url,concerns,score):
		self.name = name
		self.url = url
		self.concerns = concerns
		self.score = score

class Detail:
	def __init__(self,id,name,imgUrl,href,product):
		self.id = rowId
		self.name = name 
		self.imgUrl = imgUrl
		self.href = href
		self.product = product
		self.ingredients = []
	def addIngredient(d=Ingredient):
		self.ingredients.append(d)
	def toJson(self):
		return json.dumps(self.__dict__)

def parse_html(f_name):
	lst=[]
	f = open(f_name,'r')
	id = f_name[7:-5]
	print id
	body = f.read()
	sel = Selector(text=body)
	#values = sel.xpath('//span[@class="dark"]/text()').extract()[0]
	name = sel.xpath('//div[@id="righttoptitleandcats"]/h1/text()').extract()[0]
	desc = sel.xpath('//div[@id="summary_paragraph"]/text()').extract()[0]
	imgUrl = sel.xpath('//div[@class="right2012product_left fleft"]//@src').extract()[0]
	rows1 = sel.xpath('//div[@class="individualbar_3col"]')
	for row in rows1:
		field = row.xpath('div[@class="individualbar_col1 fleft"]')
		field = field.xpath('string(.)').extract()[0]
		score = row.xpath('div[@class="individualbar_col2 fleft"]//@style').extract()[0]
		score = float(score[6:-2])/1.9
		print '--------',field,'---',score
	rows = sel.xpath('//table[@class="product_tables"]/tbody/tr')
	#print name,imgUrl,desc
	
	#for tr in rows:


if __name__ == '__main__':
	parse_html('detail/100002.html')

	