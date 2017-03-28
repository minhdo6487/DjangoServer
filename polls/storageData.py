import json

class storageData:
    def __init__(self):
        pass
    @classmethod
    def jsonData(cls,urlSubLink,headerH1):
        return {
            'urlSubLink':urlSubLink,
            'headerH1':headerH1
        }
    @classmethod
    def jsonSave(cls,jsonData,fileID):
        with open(fileID,'w') as f:
            json.dump(jsonData,f,indent=4)