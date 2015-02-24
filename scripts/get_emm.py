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
lang = 'it'
ctrs = ['AT','BE','BA','BG','HR','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LT','MK','MD','ME','NL','NO','PL','PT','RO','RU','RS','SK','SI','ES','SE','CH','GB']


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
			print "========" 
			dup = db.articles.find_one({"link":obj['link']})
			
			if(dup is not None):
				
				print "we have it already"
				print dup['title'].encode('utf-8')
				rows.append(dup["_id"])
				continue

			else:
				print 
				print "new article"
				obj['title'] = r.contents[1].text.encode('utf-8')
				#print r.contents[3]
				print obj['title']
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

	exact = ""
	page = 0

	if "page" in query:
		page = query["page"]

	if "exact" in query:
		exact = query["exact"]

	allw = query["all"]

	res = []
	thispage = ""
	print "begin"
	

	while thispage is not None:

		page = page+1

		payload = {
		'edition': 'searcharticle', 
		'option': 'advanced', 
		'language':'en',
		'all': allw,
		'exact' : exact,
		'dateFrom': start,
		'dateTo': end,
		'page': page,
		'lang' : langs,
		'sourceCountry' : ','.join(countries)
		}

		r = None

		print "going for page " + str(page)
		try:
			r = requests.get(baseurl, params=payload,timeout=10.0)
		except:
			print "timed out"
			continue

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

		

queries_list = [
     
    {
        "all": "arma ucciso",
        "page": 529
    }, 
    {
        "all": "arma uccisione"
    }, 
    {
        "all": "rivoltella omicidio"
    }, 
    {
        "all": "rivoltella assassinato"
    }, 
    {
        "all": "rivoltella suicidio"
    }, 
    {
        "all": "rivoltella morte"
    }, 
    {
        "all": "rivoltella morto"
    }, 
    {
        "all": "rivoltella assassinio"
    }, 
    {
        "all": "rivoltella assassinare"
    }, 
    {
        "all": "rivoltella assassinato"
    }, 
    {
        "all": "rivoltella uccidere"
    }, 
    {
        "all": "rivoltella ucciso"
    }, 
    {
        "all": "rivoltella uccisione"
    }, 
    {
        "all": "fucile omicidio"
    }, 
    {
        "all": "fucile assassinato"
    }, 
    {
        "all": "fucile suicidio"
    }, 
    {
        "all": "fucile morte"
    }, 
    {
        "all": "fucile morto"
    }, 
    {
        "all": "fucile assassinio"
    }, 
    {
        "all": "fucile assassinare"
    }, 
    {
        "all": "fucile assassinato"
    }, 
    {
        "all": "fucile uccidere"
    }, 
    {
        "all": "fucile ucciso"
    }, 
    {
        "all": "fucile uccisione"
    }, 
    {
        "all": "sparare omicidio"
    }, 
    {
        "all": "sparare assassinato"
    }, 
    {
        "all": "sparare suicidio"
    }, 
    {
        "all": "sparare morte"
    }, 
    {
        "all": "sparare morto"
    }, 
    {
        "all": "sparare assassinio"
    }, 
    {
        "all": "sparare assassinare"
    }, 
    {
        "all": "sparare assassinato"
    }, 
    {
        "all": "sparare uccidere"
    }, 
    {
        "all": "sparare ucciso"
    }, 
    {
        "all": "sparare uccisione"
    }, 
    {
        "all": "tiro omicidio"
    }, 
    {
        "all": "tiro assassinato"
    }, 
    {
        "all": "tiro suicidio"
    }, 
    {
        "all": "tiro morte"
    }, 
    {
        "all": "tiro morto"
    }, 
    {
        "all": "tiro assassinio"
    }, 
    {
        "all": "tiro assassinare"
    }, 
    {
        "all": "tiro assassinato"
    }, 
    {
        "all": "tiro uccidere"
    }, 
    {
        "all": "tiro ucciso"
    }, 
    {
        "all": "tiro uccisione"
    }, 
    {
        "all": "sparatoria omicidio"
    }, 
    {
        "all": "sparatoria assassinato"
    }, 
    {
        "all": "sparatoria suicidio"
    }, 
    {
        "all": "sparatoria morte"
    }, 
    {
        "all": "sparatoria morto"
    }, 
    {
        "all": "sparatoria assassinio"
    }, 
    {
        "all": "sparatoria assassinare"
    }, 
    {
        "all": "sparatoria assassinato"
    }, 
    {
        "all": "sparatoria uccidere"
    }, 
    {
        "all": "sparatoria ucciso"
    }, 
    {
        "all": "sparatoria uccisione"
    }, 
    {
        "all": "omicidio", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "assassinato", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "suicidio", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "morte", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "morto", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "assassinio", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "assassinare", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "assassinato", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "uccidere", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "ucciso", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "uccisione", 
        "exact": "aprire il fuoco"
    }, 
    {
        "all": "omicidio", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "assassinato", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "suicidio", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "morte", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "morto", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "assassinio", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "assassinare", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "assassinato", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "uccidere", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "ucciso", 
        "exact": "aperto il fuoco"
    }, 
    {
        "all": "uccisione", 
        "exact": "aperto il fuoco"
    }
]

for q in queries_list:

	queryEMM(q)




