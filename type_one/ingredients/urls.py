from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'meal'

urlpatterns = [
    path('', views.ingredients, name='ingredients')
]
