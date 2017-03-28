from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Choice, Question, UrlNav, SubUrlNav, Restaurant, User
from polls.crawlData import crawlData, crawlSpecificCss
from polls.storageData import storageData
from polls.dumpModelToJson import dumpModelToJson
from polls.googemap import SearchGoogleMap
from django import forms
from .form import PollsRestaurant

class IndexView(generic.ListView):

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class AddressForm(forms.Form):
    address = forms.CharField()

def listrestaurant(request):
    listNameRes = []
    if request.POST:
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            print(address)

    for item in Restaurant.objects.all():
        listNameRes.append(item.restaurantName)
    context = {
        'res_list' : listNameRes,
        'form': form
    }
    return render(request, 'polls/listRestaurant.html', context)

def ResultCrawlData(request):
    queryset = UrlNav.objects.all()
    context = {
        'object_list':queryset,
    }
    return render(request,'polls/renderCrawlData.html',context)

def GoogleMap(request):
    listNameRes = []
    listAddressRes = []
    restaurantIndex = 1
    form = AddressForm()
    if request.POST:
        form = AddressForm(request.POST)
        if form.is_valid():
            restaurantIndex = form.cleaned_data['address']
            print(restaurantIndex)

    lat, lng = SearchGoogleMap.searchAddress(
        address= Restaurant.objects.get(pk=restaurantIndex).restaurantAddress
    )
    for item in Restaurant.objects.all():
        listNameRes.append(item.restaurantName)
        listAddressRes.append(item.restaurantAddress)
    context = {
        'lat':lat,
        'lng':lng,
        'nameRestaurant': Restaurant.objects.get(pk=restaurantIndex).restaurantName,
        'form':form,
        'res_list_name': listNameRes,
        'res_list_address': listAddressRes
    }
    return render(request,'polls/googlemap.html',context)

def ResultCrawlSubData(request):
    queryset = SubUrlNav.objects.all()
    context = {
        'object_list':queryset,
    }
    return render(request,'polls/renderCrawlData.html',context)

def search(request,restaurant_id):
    restaurant = Restaurant.objects.get(pk = restaurant_id)
    lat, lng = SearchGoogleMap.searchAddress(
        address=Restaurant.objects.get(pk=restaurant_id).restaurantAddress
    )
    context = {
        'restIndex': restaurant.id,
        'lat': lat,
        'lng': lng,
        'nameRestaurant': Restaurant.objects.get(pk=restaurant_id).restaurantName
    }
    return render(request, 'polls/googlemap.html', context)
    #return HttpResponseRedirect(reverse(context,'polls:googlemap', args=(restaurant.id,)))

def vote(request, question_id ):
    listsubmodel = []
    for item in UrlNav.objects.all():
        try:
            urlsublink = UrlNav.objects.get(navigation_link__contains=item.navigation_link)
            listsubmodel.append(
                dumpModelToJson.dumpToJson(
                    listData= urlsublink.suburlnav_set.all()
                )
            )
        except:
            pass
    fileID = 'dataNavLinkfromWeb.json'
    storageData.jsonSave(jsonData= listsubmodel, fileID= fileID)

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #return HttpResponseRedirect(reverse('polls:results', args=(Question.objects.get(pk=1).choice_set.all())))
        #return HttpResponse(listsubmodel)


def restaurant_create(request):

    form = PollsRestaurant(request.POST or None, request.FILES or None)
    if form.is_valid():
        restaurantName = (request.POST.get('restaurantName'))
        restaurantAddress = (request.POST.get('restaurantAddress'))
        infoRestaurant = Restaurant.objects.create(
            restaurantName = restaurantName,
            restaurantAddress = restaurantAddress
        )
        infoRestaurant.save()
    context = {
        'form': form
    }
    return render(request, 'polls/polls_form.html', context)

def restaurant_update(request, pk=None, ):
    form = PollsRestaurant()
    restaurantName = ''
    restaurantAddress = ''
    instance = get_object_or_404(Restaurant, pk= pk)
    form = PollsRestaurant(request.POST or None, request.FILES or None, instance =instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        'form': form,
        'restaurantName':restaurantName,
        'restaurantAddress':restaurantAddress
    }
    return render(request, 'polls/polls_form.html', context)
