from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice
from .forms import QuestionForm, ChoiceFormSet


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now())  # .order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    # context_object_name = 'question'
    template_name = 'polls/detail.html'
    # * el contexto es puesto automaticamente


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # te lleva a al formulario
        return render(request, 'polls/detail.html',
                      {"question": question,
                       "error_message": "No seleccionaste ninguna opcion"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # reverse -> "/polls/3/results/"
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class CreatePollView(generic.CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'polls/create_poll.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['choices'] = ChoiceFormSet(self.request.POST)
        else:
            data['choices'] = ChoiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        form.instance.pub_date = timezone.now()
        self.object = form.save()
        if choices.is_valid():
            choices.instance = self.object
            choices.save()
        return super().form_valid(form)



# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return HttpResponse(render(request, "polls/index.html", context))
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {"question": question})
