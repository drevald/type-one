from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', list, name='list'),
    path('records', list, name='list'),
    path('records/create', create, name='create'),
    path('records/long', long, name='long'),
    # path('records/store', store, name='store'),
    path('records/<int:pk>/', details, name='details'),
    path('records/<int:pk>/delete', delete, name='delete'),
]


