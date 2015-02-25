from newspaper import Article
from pymongo import MongoClient
import signal
from textrazor import TextRazor

client = MongoClient();
db = client.fire


def handler(signum, frame):
	print('Signal handler called with signal', signum)
	raise OSError("Timeout :/")


def callEntities(txt,k):

	signal.signal(signal.SIGALRM, handler)
	signal.alarm(10)


	cli = TextRazor(api_key=k, extractors=["entities", "topics"])
	#cli.set_entity_allow_overlap(False)
	#cli.set_enrichment_queries(["fbase:/location/location/geolocation>/location/geocode/latitude","fbase:/location/location/geolocation>/location/geocode/longitude"])

	response = cli.analyze(txt)

	signal.alarm(0)

	return response


def getFullText():

	arts = db.articles.find( { "lang":"it","fulltext" : { "$exists" : False }, "excluded" : { "$exists" : False }},timeout=False)

	for row in arts:
		try:
			article = Article(row['link'])
			article.download()
			article.parse()

			print 'article parsed'
			txt = article.text
			row['fulltext'] = txt.encode("utf-8")
			db.articles.update({"_id":row["_id"]},{"$set":{"fulltext":row['fulltext']}})
			
		except:
			try:
				db.articles.update({"_id":row["_id"]},{"$set":{"excluded":True, "ft-error":True}})
			except:
				print "error! error! error! "+row["_id"]
				continue
			continue
		
		



def cleanDuplicates():
	toClean = db.articles.aggregate([
	  { "$group": { 
	    "_id": { "firstField": "$title" }, 
	    "uniqueIds": { "$addToSet": "$_id" },
	    "count": { "$sum": 1 } 
	  }}, 
	  { "$match": { 
	    "count": { "$gt": 1 } 
	  }}
	])

	for t in toClean["result"]:
		for a in t["uniqueIds"][1:]:

			db.articles.update({"_id":a},{'$set':{'duplicate': True,'excluded': True}})


def getNER():

	c=0
	key1="a927283657587fd8d4e17615471c22dabfd2ee379ab2935a4b75a2c5"
	key2="14c0ac70b96530e1564c9008ceda0b050b13391797f4cda7688f482a"

	arts = db.articles.find( { "lang": "it", "entities" : { "$exists" : False }, "excluded" : { "$exists" : False }, "fulltext" : {"$exists":True,"$ne":""}} )

	for row in arts:
		k = ""
		tries = 0
		c = c+1

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
					response = callEntities(unicode(row["fulltext"]),k)
			except Exception,e:
				print e
				tries = tries+1
				continue
			break


		if tries >5:
			db.articles.update({"_id":row["_id"]},{'$set':{'ner-error': True,'excluded': True}})
			continue

		print response

		try:

			for p in response.entities():
				row['entities'].append({"id":p.id, "confidence":p.confidence_score,"types":p.dbpedia_types,"relevance":p.relevance_score,"text":p.matched_text,"freebase_types":p.freebase_types})
				
			for p in response.topics():
				row['topics'].append({"label":p.label,"score":p.score})

			db.articles.update({"_id":row["_id"]},{'$set':{'entities': row["entities"],'topics': row["topics"]}})

		except Exception,e:
			print e
			db.articles.update({"_id":row["_id"]},{'$set':{'ner-error': True,'excluded': True}})
			continue

		print 'entities retrieved'


getFullText()
