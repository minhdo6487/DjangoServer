import googlemaps
key_api_googlemap = 'AIzaSyBHNHpEqZKpOCU9YJBa8JP3sBvszZ0OzjY'

class SearchGoogleMap:
    def __init__(self):
        pass
    @classmethod
    def searchAddress(cls,address):
        gmaps = googlemaps.Client(key = key_api_googlemap)
        geocode_result = gmaps.geocode(address)
        latitudeFindOnMap = geocode_result[0]['geometry']['location']['lat']
        longitudeFindOnMap = geocode_result[0]['geometry']['location']['lng']
        return latitudeFindOnMap, longitudeFindOnMap
        #return geocode_result
