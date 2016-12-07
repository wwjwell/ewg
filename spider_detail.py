# -*- coding: utf-8 -*-
import urllib2,zlib
import thread,random
class D:
	def __init__(self,id,url):
		self.id = id
		self.url = url


def spider(lst):
	headers = [
	    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
	    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; InfoPath.1',
	    'Mozilla/4.0 (compatible; GoogleToolbar 5.0.2124.2070; Windows 6.0; MSIE 8.0.6001.18241)',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; Sleipnir/2.9.8)',
	    #因篇幅关系,此处省略N条
	]
	for d in lst:
		url = 'http://www.ewg.org%s' % d.url
		fname = 'detail/%s.html' % d.id
		random_header = random.choice(headers)
		# 可以通过print random_header查看提交的header信息
		# req_header={
		# 	"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML:like Gecko) Version/9.1.2 Safari/601.7.7',
		# 	'Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		# 	'Accept-Encoding','gzip:deflate:sdch',
		# 	'Accept-Language','zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2',
		# 	'Connection','keep-alive',
		# 	'Cache-Control','max-age=0',
		# 	'Upgrade-Insecure-Requests','1',
		# 	'Cookie','__cfduid=dd9fdb5ef24d49d1d814212140ede81da1480940507; optimizelyEndUserId=oeu1480940511893r0.5492793782360426; splash_2016yea=Y; saw_yea=yes; sawsplash=yes; optimizelySegments=%7B%22197395253%22%3A%22referral%22%2C%22197845425%22%3A%22false%22%2C%22197868052%22%3A%22gc%22%2C%227006273488%22%3A%22gc%22%2C%227029951165%22%3A%22referral%22%2C%227038420664%22%3A%22false%22%7D; optimizelyBuckets=%7B%7D; sd3_items_viewed=584324%2C512312%2C; sd3_shopping_basket=; sd3_products=0; sd3_search_history=; sd3_atatime=10; testcookie=Y; __atuvc=76%7C49; __atuvs=5846a7d96b33523d003; _ga=GA1.2.660152943.1480940513; __utma=232508224.660152943.1480940513.1480957257.1481025499.5; __utmb=232508224.8.10.1481025499; __utmc=232508224; __utmz=232508224.1480940513.1.1.utmcsr=mail.weidian.com|utmccn=(referral)|utmcmd=referral|utmcct=/cgi-bin/readmail',
		# 	'Host':'www.ewg.org',
		# 	'Referer':'http://www.ewg.org/'}
		req = urllib2.Request(url)
		req.add_header("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7')
		req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('Accept-Encoding','gzip, deflate, sdch')
		req.add_header('Accept-Language','zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2')
		req.add_header('Connection','keep-alive')
		req.add_header('Cache-Control','max-age=0')
		req.add_header('Upgrade-Insecure-Requests','1')
		#req.add_header('Cookie','__cfduid=dd9fdb5ef24d49d1d814212140ede81da1480940507; optimizelyEndUserId=oeu1480940511893r0.5492793782360426; splash_2016yea=Y; saw_yea=yes; sawsplash=yes; optimizelySegments=%7B%22197395253%22%3A%22referral%22%2C%22197845425%22%3A%22false%22%2C%22197868052%22%3A%22gc%22%2C%227006273488%22%3A%22gc%22%2C%227029951165%22%3A%22referral%22%2C%227038420664%22%3A%22false%22%7D; optimizelyBuckets=%7B%7D; sd3_items_viewed=584324%2C512312%2C; sd3_shopping_basket=; sd3_products=0; sd3_search_history=; sd3_atatime=10; testcookie=Y; __atuvc=76%7C49; __atuvs=5846a7d96b33523d003; _ga=GA1.2.660152943.1480940513; __utma=232508224.660152943.1480940513.1480957257.1481025499.5; __utmb=232508224.8.10.1481025499; __utmc=232508224; __utmz=232508224.1480940513.1.1.utmcsr=mail.weidian.com|utmccn=(referral)|utmcmd=referral|utmcct=/cgi-bin/readmail')
		req.add_header('Host', 'www.ewg.org')
		req.add_header('Referer', 'http://www.ewg.org/')
		#req.add_header('GET', url)
		try:
			resp = urllib2.urlopen(req,timeout=10)
			respInfo = resp.info();
			respHtml = resp.read();
			resp.close()
			if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
				respHtml = zlib.decompress(respHtml, 16+zlib.MAX_WBITS);
			f = open(fname,'wb')
			f.write(respHtml)
			f.close()
		except:
			print 'TIMEOUT %s %s' % (d.id,d.url)
def thread_run():
	f = open('detail_url.txt','r')
	d_map = {}

	idx = 0
	t_len = 100
	for url in f.readlines():
		id = url.split("/")[3]
		d = D(id,url)
		lst = d_map.get(idx%t_len,[])
		lst.append(d)
		d_map[idx%t_len] = lst
		idx += 1

	for i in range(t_len):
		try:
			thread.start_new_thread( spider, (d_map[i],))
		except:
			print "Error: unable to start thread"

def err_run():
	f = open('error.out','r')
	lst=[]
	for line in f.readlines():
		if len(line.strip()) >0 :
			s=line.split(' ')
			d = D(s[1],s[2])
			lst.append(d)
			
	spider(lst)
		

if __name__ == '__main__':
	err_run()
	
	
