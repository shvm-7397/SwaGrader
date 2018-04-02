from django.shortcuts import render
from django.views import generic
from .models import *
from judge import falcon


# Create your views here.


def index(request):
    """ To display list of all active, upcoming and Past Contests """
    active = Challenge.objects.filter(status='Active')
    upcoming = Challenge.objects.filter(status='Upcoming')
    past = Challenge.objects.filter(status='Past')
    context = {
        'active': active,
        'upcoming': upcoming,
        'past': past
    }
    return render(request, 'contests/index.html', context)


class DetailView(generic.DetailView):
    """ To Display list of problems in a Contest """
    model = Challenge
    template_name = 'contests/contest_page.html'
    context_object_name = 'contest'


def problem_page(request, contest_id, pk):
    problem_id = pk
    context = {
        'current_user': None,
        'current_challenge': Challenge.objects.get(pk=contest_id),
        'problem': Problem.objects.get(pk=problem_id),
    }
    if request.user.is_authenticated:
        context['current_user'] = request.user

    if request.method == 'GET':
        # Display a single problem
        return render(request, 'contests/prob-placeholder.html', context)

    elif request.method == 'POST':
        # Code Submission and Evaluation
        submission = Submission()
        submission.user = request.user
        submission.problem = Problem.objects.get(pk=problem_id)
        submission.language = request.POST['language-choice']
        submission.source_file = request.FILES['src-file']
        submission.status = 'Checking'
        submission.save()

        result = falcon.eval_submission(problem_code=submission.problem.problem_code,
                                        src_file_name=submission.source_file.name,
                                        language=submission.language)
        submission.status = context['response'] = result[0]
        submission.save()

        # Update score of the user in the particular contest, particular problem.
