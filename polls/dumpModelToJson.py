from django.core import serializers
import json

class dumpModelToJson:
    def __init__(self):
        pass
    @classmethod
    def dumpToJson(cls, listData):
        dataGetfromModel = serializers.serialize('json', listData)
        return eval(dataGetfromModel)
        # dataGetfrommodel = serializers.serialize('json', Question.objects.all())
        #pre_spareData = json.dumps(dataGetfrommodel)