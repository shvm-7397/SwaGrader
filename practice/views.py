from django.shortcuts import render
from contests.models import Problem, Submission
from judge import falcon
from swagrader.settings import BASE_DIR
# Create your views here.


def practice_problems(request):
    """ Display all Practice Problems """
    context = {'problems': Problem.objects.filter(in_practice=True)}
    return render(request, "practice/practice-section.html", context)


def practice_problem_page(request, pk):
    problem_id = pk
    context = {
        'current_user': None,
        'current_challenge': 'Practice',
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
        return render(request, 'contests/sub_response.html', context)
