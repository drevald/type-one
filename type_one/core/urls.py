from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', list, name='list'),
    path('records/', list, name='list'),
    path('records/create/<int:type>', create, name='create'),
    path('records/<int:pk>/', details, name='details'),
    path('records/<int:pk>/delete', delete, name='delete'),
]