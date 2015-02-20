from bs4 import BeautifulSoup
import datetime, requests, re, pymongo
from pymongo import MongoClient

format = '%Y-%m-%d %H:%M:%S'
format2 = '%A, %B %d, %Y %I:%M:%S %p %Z'

client = MongoClient();
db = client.fire


def handler(signum, frame):
	print('Signal handler called with signal', signum)
	raise OSError("Timeout :/")

baseurl = 'http://emm.newsbrief.eu/NewsBrief/dynamic?edition=searcharticles&option=advanced'

language = 'en'
dateFrom = '2010-01-01'
dateTo = datetime.date.today().strftime("%Y-%m-%d")
exact = ''
lang = 'en'
ctrs = ['AT','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LT','MK','MD','ME','NL','NO','PL','PT','RO','RU','RS','SK','SI','ES','SE','CH']


'''language=it&page=16&dateFrom=2012-01-01&exact=procrastination&lang=en&sourceCountry=AT&sourceCountry=BE&sourceCountry=BA&sourceCountry=BG&sourceCountry=HR&sourceCountry=CZ&sourceCountry=DK&sourceCountry=EE&sourceCountry=FI&sourceCountry=FR&sourceCountry=DE&sourceCountry=GR&sourceCountry=HU&sourceCountry=IS&sourceCountry=IE&sourceCountry=IT&sourceCountry=LV&sourceCountry=LT&sourceCountry=MK&sourceCountry=MD&sourceCountry=ME&sourceCountry=NL&sourceCountry=NO&sourceCountry=PL&sourceCountry=PT&sourceCountry=RO&sourceCountry=RU&sourceCountry=RS&sourceCountry=SK&sourceCountry=SI&sourceCountry=ES&sourceCountry=SE&sourceCountry=CH&_=1423837830314'''


def scrapePage(html):

	rows = []
	soup = BeautifulSoup(html)
	res = soup.select('.articlebox_big')

	if len(res) == 0:
		return None
	else:
		for r in res:
			obj={}
			

			obj['link'] = r.contents[1].a['href']
			
			dup = db.articles.find_one({"link":obj['link']})
			
			if(dup is not None):
				print "we have it already"
				rows.append(dup["_id"])
				continue

			else:
				print "new article"
				obj['title'] = r.contents[1].text.encode('utf-8')
				#print r.contents[3]
				obj['journal'] = r.contents[3].a.text

				spl = r.contents[3].img['src'].split("/")
				obj['country'] = spl[len(spl)-1].split(".")[0]

				dt = list(r.contents[3].stripped_strings)
				
				m = re.search('(.*) (CET|CEST)', dt[1])
				obj['time'] = datetime.datetime.strptime(m.group(0),format2)
				
				try:
					aid = db.articles.insert(obj)
					rows.append(aid)

				except pymongo.errors.DuplicateKeyError:
					continue


		return rows


def queryEMM(query, start = dateFrom, end = dateTo, langs = lang, countries = ctrs):

	res = []
	thispage = ""
	print "begin"
	page = 0

	while thispage is not None:

		page = page+1

		payload = {
		'edition': 'searcharticle', 
		'option': 'advanced', 
		'language':'en',
		'all': query,
		'dateFrom': start,
		'dateTo': end,
		'page': page,
		'lang' : langs,
		'sourceCountry' : ','.join(countries)
		}


		print "going for page " + str(page)
		r = requests.get(baseurl, params=payload)

		thispage = scrapePage(r.text)

		if(thispage is not None):
			res = res + thispage


	#query metadata
	fin = {
	"query":query,
	'dateFrom': start,
	'dateTo': end,
	'lang' : langs,
	'sourceCountry' : ','.join(countries),
	"processed" : False,
	"articles":res
	}

	db.queries.insert(fin)

		


queryEMM("shoot death")




