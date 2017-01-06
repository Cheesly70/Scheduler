from django.conf.urls import url
from django.views.generic import ListView, DetailView
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),

]
