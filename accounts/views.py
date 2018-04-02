from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.


def home(request):
    """ To Display User Profile """
    context = {'current_user': None}
    if request.user.is_authenticated:
        context['current_user'] = request.user
    return render(request, 'accounts/profile.html', context)


@login_required
def update(request):
    """ For Updating User Profile """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
        return redirect('accounts:accounts-home')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/update_form.html', {
        'profile_form': profile_form
    })


class UserFormView(View):
    """ For Creating a User Account """
    form_class = UserForm
    template_name = 'accounts/signup_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:accounts-update')  # Success page

        return render(request, self.template_name, {'form': form})


def login_view(request):
    """ For User Login """
    if request.method == 'GET':
        return render(request, 'accounts/login_form.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')  # Success page
        else:
            return render(request, 'accounts/login_form.html', {})


def logout_view(request):
    """ For Logout """
    logout(request)
    return redirect('home:home')

