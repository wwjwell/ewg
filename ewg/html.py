# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.selector import Selector

f = open('../blush.html','r')
body = f.read()
sel = Selector(text=body)
values = sel.xpath('//span[@class="dark"]/text()').extract()[0]
print int(values.replace(',', ''))

rows = sel.xpath('//table[@id="table-browse"]/tbody/tr[position()>1]')
#print rows
for tr in rows:
	id = tr.xpath('./td[1]/text()').extract()[0]
	image = tr.xpath('./td[2]//@src').extract()[0]
	url = tr.xpath('./td[3]//@href').extract()[0]
	name = tr.xpath('./td[3]//text()').extract()[0]
	print id,url,image,name
	