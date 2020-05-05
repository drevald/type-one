from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'meal'

urlpatterns = [
    path('', ingredients, name='ingredients')
]
