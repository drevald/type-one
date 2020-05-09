from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'ingredients'

urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('fetch/', views.fetch, name='fetch'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
