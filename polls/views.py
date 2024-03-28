from django.shortcuts import render, get_object_or_404
from . import models
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone


###### old function based index view ################
######################################################
# displays the latest few questions.
# def index(request):
#     questions = models.Question.objects.order_by('-pub_date')[:2]
#     context = {
#         'latest_questions_list': questions
#     }
#     return render(request, 'polls\index.html' ,context)

############### generic index view ###################
######################################################
class index(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return models.Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:2]






###### old function based detail view ################
######################################################
#  displays a question text, with no results but with a form to vote.
# def detail(request, question_id):
#     question = get_object_or_404(models.Question, pk=question_id)
#     context = {
#             'question': question
#     }    
#     return render(request, 'polls\detail.html', context)

############### generic detail view ###################
######################################################
class detail(generic.DetailView):
    template_name = 'polls/detail.html'
    context_object_name = 'question'
   # model = models.Question
    def get_queryset(self):
        return models.Question.objects.filter(pub_date__lte=timezone.now())    





###### old function based result view ################
######################################################
# displays results for a particular question.
# def result(request, question_id):
#     question = get_object_or_404(models.Question, pk=question_id)
#     return render(request, 'polls/result.html', {
#         'question':question
#     })

############### generic result view ###################
######################################################
class result(generic.DetailView):
    template_name = 'polls/result.html'
    model = models.Question





# handles voting for a particular choice in a particular question.
def action(request, question_id):

    question = get_object_or_404(models.Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, models.Choice.DoesNotExist):
        return render(request, 'polls\detail.html', {
            'question': question,
            'error_message': 'you didn\'t select a choice'
        })

    else:
        selected_choice.votes+=1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
       
