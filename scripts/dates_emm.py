from pymongo import MongoClient
import dateutil.parser
from datetime import datetime, date, time
import json



client = MongoClient();
db = client.fire
collection = db.test
lst = []


a = collection.aggregate([{"$project":{"day":{"$dayOfMonth":'$time'},"month":{"$month":'$time'},"year":{"$year":'$time'}}},{"$group":{"_id":{"day":'$day',"month":'$month',"year":'$year'}, "count": {"$sum":1}}}])


for b in a["result"]:
	lst.append({"date":date(b["_id"]["year"],b["_id"]["month"],b["_id"]["day"]),"count":b["count"]})

lst.sort(key=lambda x: x["date"], reverse=True)

for c in lst:
	c["date"] = c["date"].isoformat()


with open('result.json', 'w') as fp:
    json.dump(lst, fp)