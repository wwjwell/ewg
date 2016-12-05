# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.selector import Selector


#sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib /Library/Python/2.7/site-packages/MySQL_python-1.2.4b4-py2.7-macosx-10.11-intel.egg/_mysql.so

class ListSpider(scrapy.Spider):
	def __init__(self):
		self.page = 1
		self.total = 10
	name = "ewg"
	allowed_domains = ["ewg.org"]
	start_urls = ["http://www.ewg.org/skindeep/browse/blush/"]

	def parse(self,response):
		url = response.url
		file_name = 'blush/%d.html' % self.page
		f = open('blush/%d.html' % self.page,'wb')
		f.write(response.body)
		f.close()
		if self.page == 1:
			sel = Selector(text=response.body)
			rows = sel.xpath('//table[@id="table-browse"]/tbody/tr[position()>1]')
			self.total = int(sel.xpath('//span[@class="dark"]/text()').extract()[0].replace(',', ''))
			print "total=",self.total
		
		start = self.page * 10 
		self.page = self.page +1
		if start>self.total:
			return
		print "spider page = %d" % (self.page-1)
		next_url="http://www.ewg.org/skindeep/browse.php?category=blush&showmore=products&start=%d" % (self.page*10)
		yield scrapy.Request(next_url, callback=self.parse)

	