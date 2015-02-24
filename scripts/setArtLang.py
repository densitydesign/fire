from pymongo import MongoClient
import dateutil.parser
from datetime import datetime, date, time
import json


client = MongoClient();
db = client.fire


queries = db.queries.find()

for q in queries:
	if 'lang' in q:
		print q['query']
		print len(q['articles'])
		for art in q['articles']:
			article = db.articles.update({"_id":art},{"$set": {"lang": q['lang']}})