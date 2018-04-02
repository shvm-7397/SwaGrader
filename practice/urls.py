from django.conf.urls import url
from .import views

app_name = 'practice'

urlpatterns = [
    url(r'^$', views.practice_problems, name='practice-home'),
    url(r'^problem/(?P<pk>[0-9]+)/$', views.practice_problem_page, name='practice-problem'),
]
