from .models import Restaurant
import json, requests
from elasticsearch import Elasticsearch
from polls.dumpModelToJson import dumpModelToJson
from polls.googemap import key_api_googlemap, SearchGoogleMap


class RestaurantIndex:
    def __init__(self):
        pass
    @classmethod
    def bulkRestaurant(cls, pattern):
        data = ''
        for res in Restaurant.objects.all():
            data += '{"index": {"_id": "%s"}}\n' % res.pk
            data += json.dumps({
                "restaurantName": res.restaurantName,
                "restaurantAddress":res.restaurantAddress,
            })+'\n'
        response = requests.put('http://127.0.0.1:9200/index/polls/_bulk', data = data)
        data = {
            "query" : {
                "query_string": {
                    "query" : pattern
                }
            }
        }
        response = requests.post('http://127.0.0.1:9200/index/polls/_search', data=json.dumps(data))
        return response.json()

### stuck not work ###
class RestaurantAPI:
    def __init__(self):
        pass
    @classmethod
    def esAPI(cls):
        r = requests.get('http://localhost:9200')
        countIndex = 1
        es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        while r.status_code == 200:
            r = requests.get('http://localhost:8000/api/polls/' + str(countIndex) + '/')
            es.index(index='restaurant', doc_type='polls', id=countIndex, body=json.loads(r.content))
            countIndex += 1
        return es
    @classmethod
    def esResttaurantInRadius(cls,ratius,address):
        lattitude, longtitude = SearchGoogleMap.searchAddress(address=address)
        es = Elasticsearch([{'host':'localhost','port':'9200'}])
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        querystring = {"location": str(lattitude)+','+str(longtitude),
                       "radius": str(ratius),
                       "types": "restaurant",
                       "keyword": "Restaurant",
                       "key": key_api_googlemap}
        headers = {
            'cache-control': "no-cache",
            'postman-token': "4f32d839-798c-d6c5-3c99-0f3da276b3af"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        jsonData = json.loads(response.text)

        countIndex = 0
        for item in jsonData['results']:
            countIndex+=1
            es.index(index="nearestlocation",doc_type='googlesearch',id=countIndex, body = item)
        return es

### stuck not work ###


class RestaurantModel:
    def __init__(self):
        pass
    @classmethod
    def esModel(cls,model=None):
        es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        model = Restaurant
        modelData = dumpModelToJson.dumpToJson(listData=model.objects.all())
        countIndex = 1
        for item in modelData:
            countIndex += 1
            es.index(index = 'restaurant', doc_type='polls', id=countIndex, body=item)
        return es




