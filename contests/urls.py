from django.conf.urls import url
from .import views

app_name = 'contests'

urlpatterns = [
    url(r'^$', views.index, name='contests-home'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='contest-detail'),
    url(r'^(?P<pk>[0-9]+)/ranklist/$', views.getranklist, name='contest-ranklist'),
    url(r'^(?P<contest_id>[0-9]+)/problem/(?P<pk>[0-9]+)/$', views.problem_page, name='contest-problem'),
]
