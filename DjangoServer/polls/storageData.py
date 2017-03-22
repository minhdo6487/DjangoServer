import json

class storageData:
    def __init__(self):
        pass
    @classmethod
    def jsonData(cls,catgorizeComment,comment):
        return {
            'catgorizeComment':catgorizeComment,
            'comment':comment
        }
    @classmethod
    def jsonSave(cls,jsonData,fileID):
        with open(fileID,'w') as f:
            json.dump(jsonData,f,indent=4)