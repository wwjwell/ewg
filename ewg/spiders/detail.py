# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.selector import Selector
import category
import os
#sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib /Library/Python/2.7/site-packages/MySQL_python-1.2.4b4-py2.7-macosx-10.11-intel.egg/_mysql.so

class ListSpider(scrapy.Spider):
	name = "detail"
	allowed_domains = ["ewg.org"]
	
	def __init__(self):
		

	def get_url(self):
		return "http://www.ewg.org/skindeep/browse.php?category=%s&showmore=products&start=%d" % (self.category.category,(self.page-1)*10)

	def next(self):
		self.idx = self.idx + 1
		print "-------------------",len(self.categories),self.idx
		if self.idx <= len(self.categories):
			self.category = self.categories[self.idx-1]
			self.page = 1
			print "##############",self.category.name
			return True
		return False

	def start_requests(self):
		lst = []
		if self.next():
			url = self.get_url()
			print "NEW URL=",url
			yield scrapy.Request(url,callback = self.parse)#jump to login page

	
	def parse(self,response):
		self.log('A response from %s just arrived!' % response.url)
		print response.url
		path = "html/%s" % self.category.category
		if not os.path.exists(path):
			print "mkdir ",path
			os.makedirs(path)
		file_name = '%s/%d.html' % (path,self.page)
		f = open(file_name,'wb')
		f.write(response.body)
		f.close()
		if self.page == 1:
			sel = Selector(text=response.body)
			rows = sel.xpath('//table[@id="table-browse"]/tbody/tr[position()>1]')
			self.total = int(sel.xpath('//span[@class="dark"]/text()').extract()[0].replace(',', ''))
			print "total=",self.total
			fcount = open("%s/total.txt" % path,'wb')
			fcount.write(str(self.total))
			fcount.close()
		start = self.page * 10 
		self.page = self.page +1
		if start<self.total:
			print "spider page = %d" % (self.page-1)
			yield scrapy.Request(self.get_url(), callback=self.parse)
		elif self.next():
			yield scrapy.Request(self.get_url(),callback = self.parse)#jump to login page


	
