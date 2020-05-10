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
    path('<int:pk>/units/add', views.unit_add, name='unit_add'),
    path('<int:pk>/units/<int:unit_id>', views.unit_details, name='unit_details'),
    path('<int:pk>/units/<int:unit_id>/delete', views.unit_delete, name='unit_delete'),
]
