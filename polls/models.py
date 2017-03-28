from django.db import models
from django.conf import settings

import datetime
from polls.crawlData import crawlData, crawlSpecificCss, crawlSpecific
from polls.storageData import storageData
from polls.dumpModelToJson import dumpModelToJson
from polls.googemap import SearchGoogleMap
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import re



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

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
    suburlnav = models.ForeignKey(UrlNav, on_delete=models.CASCADE)
    subUrlNavheader = models.TextField()
    def __str__(self):
        return self.subUrlNavheader
    @classmethod
    def saveSubUrlNavTodb(cls):
        reg = 'http://www.bbc.com/'
        pattern_reg = re.compile(reg)
        for item in UrlNav.objects.all():
            listNav = []
            match= re.search(pattern_reg,item.navigation_link)
            if match:
                print(item.navigation_link)
                listNav = crawlSpecificCss.getInfoUrl(url=item.navigation_link)
                for subItem in listNav:
                    try:
                        subUrlLink = UrlNav.objects.get(navigation_link__contains=item.navigation_link)
                        subUrlLink.suburlnav_set.create(subUrlNavheader=subItem)
                        subUrlLink.save()
                    except:
                        pass

class Restaurant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    restaurantName = models.CharField(max_length=200)
    restaurantAddress = models.CharField(max_length=200)
    restaurantLatLng = models.CharField(max_length=200)
    image = models.FileField(null=True, blank=True)
    @classmethod
    def saveRestaurantTodb(cls,url):
        listRestaurant = crawlSpecific.getInfoUrl(
                                                     url=url,
                                                     typeCss='div',
                                                     classNameKey='class',
                                                     classNameValue='info'
                                                 )
        for item in listRestaurant:
            try:
                resName = item['name'].encode('ascii','ignore').decode('UTF-8')
                resAddress = item['address'].encode('ascii','ignore').decode('UTF-8')
                resLat, resLng = SearchGoogleMap.searchAddress(item['address'].encode('ascii','ignore').decode('UTF-8'))
                urlLink = Restaurant(
                    restaurantName= resName,
                    restaurantAddress= resAddress,
                    restaurantLatLng = {
                        'lat':resLat,
                        'lng':resLng
                    }
                )
                urlLink.save()
            except:
                pass
### try follow instructions ###
class BlogPost(models.Model):
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
   posted_date = models.DateField(default=timezone.now)
   title = models.CharField(max_length=200)
   text = models.TextField(max_length=1000)

