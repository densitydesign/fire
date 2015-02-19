import json, signal
import urllib
from newspaper import Article
from pymongo import MongoClient
from textrazor import TextRazor

client = MongoClient();
db = client.fire
collection = db.test


def handler(signum, frame):
	print('Signal handler called with signal', signum)
	raise OSError("Timeout :/")


def callEntities(txt):

	print "entering txtrazor"
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(10)
		
	cli = TextRazor(api_key=k, extractors=["entities", "topics"])
	response = cli.analyze(txt)	

	signal.alarm(0)

	return response


	



results = json.load(urllib.urlopen("https://www.kimonolabs.com/api/9u4k1p5g?apikey=6b34bb486749690e258fff908be14f9e"))

c=0
key1="a927283657587fd8d4e17615471c22dabfd2ee379ab2935a4b75a2c5"
key2="14c0ac70b96530e1564c9008ceda0b050b13391797f4cda7688f482a"

ln = len(results['results']['collection1'])

for row in results['results']['collection1']:
	
	c = c+1
	tries = 0

	print 'processing document ' + str(c) + "/" +str(ln)

	spl = row['lang'].split("/");
	row['lang'] = spl[len(spl)-1].split(".")[0];

	row['link'] = row['title']['href'];
	row['title'] = row['title']['text'];


	txt = row['time']['text'].split(" ");
	txt = txt[1:len(txt)-1];
	txt = ' '.join(txt)
	row['time'] = txt.split(" |")[0];

	try:
		article = Article(row['link'])
		article.download()
		article.parse()

		print 'article parsed'
		
	except:
		continue
	
	txt = article.text
	row['fulltext'] = txt.encode("utf-8")
	

	k = ""


	if c % 2 == 0:
		k = key1
	else:
		k = key2

	
	# Set the signal handler and a 5-second alarm

	response = None

	row['entities'] = []
	row['topics'] = []

	
	while True:
		try:
			if(tries<=5):
				response = callEntities(txt)
		except:
			tries = tries+1
			continue
		break


	if tries >5:
		continue

	try:

		for p in response.entities():
			row['entities'].append({"id":p.id, "confidence":p.confidence_score,"types":p.dbpedia_types,"relevance":p.relevance_score,"text":p.matched_text,"freebase_types":p.freebase_types})
			
		for p in response.topics():
			row['topics'].append({"label":p.label,"score":p.score})

	except:
		continue

	print 'entities retrieved'

	post_id = collection.insert(row)


