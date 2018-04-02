from django.shortcuts import render


def show_home(request):
    context = {'current_user': None}
    if request.user.is_authenticated:
        context['current_user'] = request.user
    return render(request, 'home/homepage.html', context)
