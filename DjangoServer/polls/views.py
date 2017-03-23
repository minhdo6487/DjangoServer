from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
#from django.urls import reverse
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Choice, Question, UrlNav, SubUrlNav
from polls.crawlData import crawlData, crawlSpecificCss
from polls.storageData import storageData
from polls.dumpModelToJson import dumpModelToJson

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

def ResultCrawlData(request):
    queryset = UrlNav.objects.all()
    context = {
        'object_list':queryset,
    }
    return render(request,'polls/renderCrawlData.html',context)

def ResultCrawlSubData(request):
    queryset = SubUrlNav.objects.all()
    context = {
        'object_list':queryset,
    }
    return render(request,'polls/renderCrawlData.html',context)

def vote(request, question_id, listDataModel=UrlNav.objects.all() ):
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
        #selected_choice.votes += 1
        #selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #return HttpResponseRedirect(reverse('polls:results', args=(Question.objects.get(pk=1).choice_set.all())))
        return HttpResponse(listsubmodel)

