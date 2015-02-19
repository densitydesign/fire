from pymongo import MongoClient
import datetime


client = MongoClient();
db = client.fire
collection = db.test
topics={}
tlist=[]
vtop=[] 
alist=[]



def euclidean(x,y):
	sumSq=0.0
	
	#add up the squared differences
	for i in range(len(x)):
		sumSq+=(x[i]-y[i])**2
		
	#take the square root of the result
	return (sumSq**0.5)


for q in collection.find():

	for t in q["topics"]:
		if t["score"]>=0.5:
			if t["label"] not in topics:
				topics[t["label"]] = {"num":1, "score":t["score"]}
			else:
				topics[t["label"]]["num"] = topics[t["label"]]["num"]+1
				topics[t["label"]]["score"] = topics[t["label"]]["score"]+t["score"]


for key, value in topics.iteritems():
	value['label'] = key;
	value['relevance'] = value['score']/value['num']
	tlist.append(value);

tlist.sort(key=lambda x: x["score"], reverse=True)


flist = tlist[0:149]
flist.sort(key=lambda x: x["relevance"], reverse=True)


for f in flist:
	print f
	vtop.append(f["score"])


for q in collection.find():
	vec=[]

	for t in flist:
		found = next((x for x in q["topics"] if x["label"] == t["label"]), None)
		if found:
			vec.append(found["score"])
		else:
			vec.append(0)

	q["distance"] = euclidean(vec,vtop)
	alist.append(q);

alist.sort(key=lambda x: x["distance"])

for a in alist:

	print [a["title"], a["distance"]]
	a['entities'].sort(key=lambda x: x["relevance"], reverse=True)
	for b in a['entities'][0:9]:
		print [b["text"],b["confidence"],b["relevance"]]
