import sys,StringIO, urllib, urllib2, cgi, re, socket
from urlparse import urlparse
import basesinfonierspout
import json

class JugandoConGoogle2(basesinfonierbolt.BaseSinfonierBolt):
	def __init__(self):
		basesinfonierbolt.BaseSinfonierBolt().__init__()

	def userprepare(self):
		self.hostname = self.getParam("hostname")

    	def userprocess(self):
    		h=self.getField(self.hostname)
    		url = 'https://www.google.com/xhtml?'		
		q = 'site:'+h
		start=0
		num=100
		gws_rd = 'ssl'
		query_string = { 'q':q, 'start':start, 'num':num, 'gws_rd':gws_rd }
		data = urllib.urlencode(query_string)
		url = url + data
		headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)', 'Referer' : 'http://127.0.0.1/'} # $
		try:
        		req = urllib2.Request(url, None, headers)
                	google_reply = urllib2.urlopen(req).read()
                	regex = '<h3 class="r"><a href="/url(.+?)">'
                	pattern = re.compile(regex)
                	url_links = re.findall(pattern, google_reply)
        	except urllib2.URLError:
                	pass

		hosts=[]
		ips=[]
	
		for url in url_links:
			url2=url.strip('?q=')
			try:
				d=urlparse(url2)
				if d.netloc not in hosts:
					hosts.append(d.netloc)	
                	except socket.error:
                        	pass


        	for host in hosts:
        		self.addField(json.dumps(host))
	   	self.emit()
               
JugandoConGoogle2().run()




