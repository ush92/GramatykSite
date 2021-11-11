from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^solution/(?P<solution_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'about', views.about, name='about'),
    url(r'profile', views.profile, name='profile'),
    url(r'^like_solution/$', views.like_solution, name='like_solution'),
    url(r'^suggest_solution/$', views.suggest_solution, name='suggest_solution'),
    url(r'^check_gramma/$', views.check_gramma, name='check_gramma'),
    # ex: /polls/5/results/
    #  url(r'^(?P<poll_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #  url(r'^(?P<poll_id>[0-9]+)/vote/$', views.vote, name='vote'),
]