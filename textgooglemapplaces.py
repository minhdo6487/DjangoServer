import requests
from elasticsearch import Elasticsearch
import json


url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

querystring = {"location":"40.7780464,-73.9786786","radius":"500","types":"restaurant","keyword":"Restaurant","key":"AIzaSyBHNHpEqZKpOCU9YJBa8JP3sBvszZ0OzjY"}

headers = {
    'cache-control': "no-cache",
    'postman-token': "4f32d839-798c-d6c5-3c99-0f3da276b3af"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
jsonData = json.loads(response.text)

#r = requests.get('http://localhost:9200')
es = Elasticsearch([{'host':'localhost', 'port':'9200'}])

id = 1
for item in jsonData['results']:
	#print(item)
	#es = elasticsearch.Elasticsearch()
	id += 1
	es.index(index='sw',doc_type='polls', id=id, body=item)
	#es.index(index='sw',doc_type='polls', id=id, body=item)
	#id += 1

