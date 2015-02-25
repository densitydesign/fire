import socks
import socket
import re
from datetime import datetime, date, time
from pymongo import MongoClient

client = MongoClient();
db = client["fire-shops"]

shop = "evolution"

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

import urllib2
import mechanize
from bs4 import BeautifulSoup

res = []
t = datetime.now().isoformat()
fin = {"created_at":t}


url = "http://k5zq47j6wd3wdvjq.onion"
#headers = {'Cookie': 'evidence=tkeemud1NdtP1F84dw5XE4MHOs8pQhDwnk99AWqTuoc='}

headers = [
    ('Cookie', 'session=eyJpdiI6IjNuK3hISlpjRFdjVTlicE9IR052bE43dFlvSHpqVXlqXC8wZmZWWjN6YThjPSIsInZhbHVlIjoiOWNjSFRMbHhVc1JYRFh0TGxRbnR5eml0d1c2NDBHUDBUNjVDWHA0V2Y5bG5wUnB5SzdkOUNFZUlhTDM4NHZZSFJIWlhJMkxXMVVOck9LRDdUdEpNQWc9PSIsIm1hYyI6ImNiMWM2MWRlNjU5MTAwYjlhNGQ0OWEwMjRjNDFiZGRkYzM4ODkwYTlhYTk4OTRjMWFjNGNjZjY5NmY0MDhlM2QifQ%3D%3D'),
    ('User-agent','Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'),
    ('Connection','keep-alive')
]


#req = urllib2.Request(url, None, headers)
#resp = urllib2.urlopen(req)
#print resp.read()

br = mechanize.Browser()
br.addheaders = headers
br.set_handle_robots(False)
br.open(url)
# follow second link with element text matching regular expression
weapons = br.follow_link(text_regex=r"Weapons", nr=0)
lethal = br.follow_link(text_regex=r"Guns", nr=0)

startUrl = lethal.geturl()

page = 1
go = True

while go:
	br.open(startUrl+"&page="+str(page))
	print startUrl+"&page="+str(page)
	page = page+1
	html = br.response().read()
	soup = BeautifulSoup(html)
	cols =  soup.select(".details .row")

	if len(cols) == 0:
		go = False
	else:
		for c in cols:

			dets = c.findAll('div')

			obj = {}
			
			
			obj['title'] = dets[0].contents[1].a.text
			obj['vendor'] = dets[0].contents[3].a.text
			#obj['descr'] = c.contents[3].span.text
			print dets[1].contents[1]
			obj['price'] = re.findall("\d+.\d+", str(dets[1].contents[1]))[0]
			print obj
			res.append(obj)



fin['items'] = res
db[shop].insert(fin)




# Now you can go ahead and scrape those shady darknet .onion sites