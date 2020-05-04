from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'meal'

urlpatterns = [
    path('', list, name='meals'),
    path('create/', create, name='create'),
]
