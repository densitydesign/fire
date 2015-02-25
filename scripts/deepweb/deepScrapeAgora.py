import socks
import socket
import re
from datetime import datetime, date, time
from pymongo import MongoClient

client = MongoClient();
db = client["fire-shops"]

shop = "agora"

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


url = "http://agorahooawayyfoe.onion"
#headers = {'Cookie': 'evidence=tkeemud1NdtP1F84dw5XE4MHOs8pQhDwnk99AWqTuoc='}

headers = [
    ('Cookie', 'evidence=tkeemud1NdtP1F84dw5XE4MHOs8pQhDwnk99AWqTuoc=')
]


#req = urllib2.Request(url, None, headers)
#resp = urllib2.urlopen(req)
#print resp.read()

br = mechanize.Browser()
br.addheaders = headers
br.open(url)
# follow second link with element text matching regular expression
weapons = br.follow_link(text_regex=r"Weapons", nr=0)
lethal = br.follow_link(text_regex=r"Lethal firearms", nr=0)

startUrl = lethal.geturl()

page = 1
go = True

while go:
	br.open(startUrl+"/"+str(page))
	print startUrl+"/"+str(page)
	page = page+1
	html = br.response().read()
	soup = BeautifulSoup(html)
	cols = soup.findAll('tr', attrs={"class" : 'products-list-item'})
	if len(cols) == 0:
		go = False
	else:
		for c in cols:
			obj = {}
			
			obj['title'] = c.contents[3].a.text
			obj['descr'] = c.contents[3].span.text

			obj['price'] = re.findall("\d+.\d+", str(c.contents[5]))[0]

			res.append(obj)

fin['items'] = res
db[shop].insert(fin)




# Now you can go ahead and scrape those shady darknet .onion sites