from django.conf.urls import url

from . import views
from .views import(
    ResultCrawlData,
    ResultCrawlSubData,
    GoogleMap,
    listrestaurant,
    restaurant_create,
    restaurant_update
)

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'create/$', restaurant_create),
    url(r'^(?P<pk>[0-9]+)/edit/$', restaurant_update, name='restaurant_update'),

    url(r'^crawldata/$',ResultCrawlData),
    url(r'^crawlsubdata/$',ResultCrawlSubData),

    url(r'^googlemap/$',GoogleMap),
    url(r'^(?P<restaurant_id>[0-9]+)/search/$', views.search, name='search'),

    url(r'^listrestaurant/$',listrestaurant)
]