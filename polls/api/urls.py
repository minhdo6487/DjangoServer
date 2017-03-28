from django.conf.urls import url
from django.contrib import admin

from .views import (
    PollsListAPIView,
    PollsCreateAPIView,
    PollsDetailAPIView
)


app_name = 'polls'
urlpatterns = [
    url(r'^$', PollsListAPIView.as_view(), name='ListAPIView'),
    url(r'^create/$', PollsCreateAPIView.as_view(), name='ListCreateAPIView'),
    url(r'^(?P<pk>[0-9]+)/$', PollsDetailAPIView.as_view(), name='ListDetailAPIView')
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    #url(r'create/$', restaurant_create),
    #url(r'^(?P<pk>[0-9]+)/edit/$', restaurant_update, name='restaurant_update'),

    #url(r'^crawldata/$',ResultCrawlData),
    #url(r'^crawlsubdata/$',ResultCrawlSubData),

    #url(r'^googlemap/$',GoogleMap),
    #url(r'^(?P<restaurant_id>[0-9]+)/search/$', views.search, name='search'),

    #url(r'^listrestaurant/$',listrestaurant)
]