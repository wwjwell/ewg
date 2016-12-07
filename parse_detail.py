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
	def __init__(self,id,name,href,concern,score,data):
		self.id = id
		self.name = name
		self.href = href
		self.concern = concern
		self.score = score
		self.data = data
	def __repr__(self):
		return repr((self.id,self.name,self.href,self.concern,self.score,self.data))

class Concern:
	def __init__(self,field,score):
		self.field = field
		self.score = score
	def __repr__(self):
		return repr((self.field, self.score))
		
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


detail_map={}
f = open('detail.txt','r')
for line in f.readlines():
	detail = json.loads(line)
	id = detail['href'].split('/')[3]
	detail_map[id] = detail


def object2dict(obj):
    #convert object to a dict
    d = {}
    d.update(obj.__dict__)
    return d
def parse_html(f_name,ingredient_f):

	lst=[]
	f = open(f_name,'r')
	id = f_name[7:-5]
	body = f.read()
	sel = Selector(text=body)
	goods = Goods()
	goods.id = id
	print 'parse ok goods.id',goods.id

	#values = sel.xpath('//span[@class="dark"]/text()').extract()[0]
	goods.name = sel.xpath('//div[@id="righttoptitleandcats"]/h1/text()').extract()[0]
	goods.desc = sel.xpath('//div[@id="summary_paragraph"]/text()').extract()
	if len(goods.desc) >0:
		goods.desc=goods.desc[0]
	else:
		goods.desc = ''
	goods.imgUrl = sel.xpath('//div[@class="right2012product_left fleft"]//@src').extract()[0]
	goods.score = sel.xpath('//div[@class="prodwrapperleftcol2012"]//img/@src').extract()[0]
	if goods.score.endswith('EWGV_SD_Mark.png'):
		goods.score = 'ewg verified'
	else:
		goods.score = goods.score[len('https://static.ewg.org/skindeep/img/draw_score/score_image'):-len('__1_.png')]
	rows1 = sel.xpath('//div[@class="individualbar_3col"]')
	detail = detail_map.get(id)
	goods.category = detail['product']
	goods.href = detail['href']
	goods.rowId = detail['rowId']

	for row in rows1:
		field = row.xpath('div[@class="individualbar_col1 fleft"]')
		field = field.xpath('string(.)').extract()[0]
		score = row.xpath('div[@class="individualbar_col2 fleft"]//@style').extract()[0]
		score = float(score[6:-2])/1.9
		concern = Concern(field,score)
		goods.concerns.append(concern)
	rows2 = sel.xpath('//div[@id="Ingredients"]//table[@class="product_tables"]/tr')
	#print name,imgUrl,desc
	for tr in rows2:
		href = tr.xpath('./td[1]//@href').extract()[0]
		name = tr.xpath('./td[1]//a/text()').extract()[0]
		concern = tr.xpath('./td[2]')
		concern = concern.xpath('string(.)').extract()[0]
		score = tr.xpath('./td[3]//div[@id="prod_cntr_score"]//a//img/@src').extract()
		if len(score) <1:
			score = tr.xpath('./td[3]//i/text()').extract()[0]
			data = 'None'
		else:
			score = score[0][len('https://static.ewg.org/skindeep/img/draw_score/score_image'):-len('__1_.png')]
			data = tr.xpath('./td[3]//div[@id="data_avail_box"]//span//text()').extract()[0]

		ingredient = Ingredient(id,name,href,concern,score,data)
		ingredient_f.write(json.dumps(ingredient,default=lambda o:o.__dict__))
		ingredient_f.write('\n')
		goods.ingredients.append(ingredient)
	ingredient_f.flush()
	return json.dumps(goods,default=lambda o:o.__dict__)


def parse_ingredient(f_name):
	f = open(f_name,'r')
	id = f_name[7:-5]
	print 'parse goods.id',id
	sel = Selector(text=f.read())
	rows2 = sel.xpath('//div[@id="Ingredients"]//table[@class="product_tables"]/tr')
	#print name,imgUrl,desc
	lst=[]
	for tr in rows2:
		href = tr.xpath('./td[1]//@href').extract()[0]
		name = tr.xpath('./td[1]//a/text()').extract()[0]
		concern = tr.xpath('./td[2]')
		concern = concern.xpath('string(.)').extract()[0]
		score = tr.xpath('./td[3]//div[@id="prod_cntr_score"]//a//img/@src').extract()
		if len(score) <1:
			score = tr.xpath('./td[3]//i/text()').extract()[0]
			data = 'None'
		else:
			score = score[0][len('https://static.ewg.org/skindeep/img/draw_score/score_image'):-len('__1_.png')]
			data = tr.xpath('./td[3]//div[@id="data_avail_box"]//span//text()').extract()[0]

		ingredient = Ingredient(id,name,href,concern,score,data)
		lst.append(ingredient)
	return lst

def runall():
	ingredient_f = open('ingredient.txt','wb')

	base_dir="detail"
	base_len=len(base_dir)
	f = open('detail_json.text','wb')
	for dirpath, _, filenames in os.walk(base_dir):
		for f_name in filenames:
			f_name = '%s/%s' % (dirpath, f_name)
			f.write(parse_html(f_name,ingredient_f))
			f.write('\n')
			f.flush()
		f.close()
		break

def runi():
	base_dir="detail"
	base_len=len(base_dir)
	f = open('ingredient.txt','wb')
	for dirpath, _, filenames in os.walk(base_dir):
		for f_name in filenames:
			f_name = '%s/%s' % (dirpath, f_name)
			for i in parse_ingredient(f_name):
				f.write(json.dumps(i,default=lambda o:o.__dict__))
				f.write('\n')
			f.flush()
		f.close()
		break
if __name__ == '__main__':
	#print parse_html('detail/486592.html')
	runall()
	