from django.db import models
import datetime
from polls.crawlData import crawlData, crawlSpecificCss
from polls.storageData import storageData
from polls.dumpModelToJson import dumpModelToJson
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class UrlNav(models.Model):
    navigation_link = models.CharField(max_length=200)
    def __str__(self):
        return self.navigation_link
    @classmethod
    def saveUrlNavTodb(cls,url):
        listNav = []
        listNav = crawlData.getInfoUrl(url=url)
        for item in listNav:
            urlLink = UrlNav(navigation_link=item)
            urlLink.save()

class SubUrlNav(models.Model):
    urlnav = models.ForeignKey(UrlNav, on_delete=models.CASCADE)
    subUrlNavheader = models.TextField()
    def __str__(self):
        return self.subUrlNavheader
    @classmethod
    def saveSubUrlNavTodb(cls,url):
        jsonData = dumpModelToJson.dumpToJson(listData=UrlNav.objects.all())

        #listDataModel = UrlNav.objects.all()
        #listNav = crawlSpecificCss.getInfoUrl(url=)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
