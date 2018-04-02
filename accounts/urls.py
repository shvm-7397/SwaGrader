from django.conf.urls import url
from .import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.home, name='accounts-home'),
    url(r'^update/$', views.update, name='accounts-update'),
    url(r'^create/$', views.UserFormView.as_view(), name='accounts-create'),
    url(r'^login/$', views.login_view, name='accounts-login'),
    url(r'^logout/$', views.logout_view, name='accounts-logout'),
]
