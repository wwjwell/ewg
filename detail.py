# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.selector import Selector
import os
import json
import category
c_map={}
for c in category.get_categories():
	c_map[str(c.category)] = c.name

class Detail:
	def __init__(self,rowId,name,imgUrl,href,product):
		self.rowId = rowId
		self.name = name 
		self.imgUrl = imgUrl
		self.href = href
		self.product = product
	def toJson(self):
		return json.dumps(self.__dict__)

def parse_html(f_name):
	lst=[]
	f = open(f_name,'r')
	body = f.read()
	sel = Selector(text=body)
	#values = sel.xpath('//span[@class="dark"]/text()').extract()[0]

	rows = sel.xpath('//table[@id="table-browse"]/tbody/tr[position()>1]')
	#print rows
	for tr in rows:
		rowId = tr.xpath('./td[1]/text()').extract()[0]
		if rowId.endswith("."):
			rowId=rowId[:-1]
		imgUrl = tr.xpath('./td[2]//@src').extract()[0]
		href = tr.xpath('./td[3]//@href').extract()[0]
		name = tr.xpath('./td[3]//text()').extract()[0]
		product = tr.xpath('./td[4]//text()').extract()
		if len(product)>0:
			product = product[0]
		else:
			product=''
		if len(href)==0:
			continue
		d = Detail(rowId,name,imgUrl,href,product)
		lst.append(d)
	return lst

def get_detail():
	base_dir="html"
	base_len=len(base_dir)
	f = open('detail.txt','wb')
	for dirpath, _, filenames in os.walk(base_dir):
		
		if len(dirpath) <= base_len+1:
			continue
		key = dirpath[base_len+1:]
		print 'Directory', dirpath,c_map[key]

		for f_name in filenames:
			f_name = '%s/%s' % (dirpath, f_name)
			if f_name.endswith('html'):
				for d in parse_html(f_name):
					f.write(d.toJson())
					f.write('\n')

def get_url():
	base_dir="list"
	base_len=len(base_dir)
	f = open('detail_url.txt','wb')
	for dirpath, _, filenames in os.walk(base_dir):
		
		if len(dirpath) <= base_len+1:
			continue
		key = dirpath[base_len+1:]
		print 'Directory', dirpath,c_map[key]

		for f_name in filenames:
			f_name = '%s/%s' % (dirpath, f_name)
			if f_name.endswith('html'):
				for d in parse_html(f_name):
					print d.href
					f.write(d.href)
					f.write('\n')
if __name__ == '__main__':
	get_url()

	