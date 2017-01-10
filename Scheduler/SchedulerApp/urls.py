from django.conf.urls import url
from django.views.generic import ListView, DetailView
from . import views

app_name ='SchedulerApp'
urlpatterns =[
    url(r'^$', views.index, name='index'),
    #url(r'^mainform/$', views.mainform, name='mainform'),
    url(r'^getmainform/$', views.getmainform, name='getmainform'),
    url(r'^processmainform/$', views.processmainform, name='processmainform'),

]
