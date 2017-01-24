from django.conf.urls import url
from django.views.generic import ListView, DetailView
from . import views

app_name ='SchedulerApp'
urlpatterns =[
    url(r'^$', views.index, name='index'),
    #url(r'^mainform/$', views.mainform, name='mainform'),
    url(r'^getmainform/$', views.get_main_form, name='get_main_form'),
    url(r'^processmainform/$', views.process_main_form, name='process_main_form'),


]
