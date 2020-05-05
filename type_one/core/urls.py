from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', list, name='list'),
    path('records/', list, name='list'),
    path('records/create/<int:type>', create, name='create'),
    path('records/<int:pk>/', details, name='details'),
    path('records/<int:pk>/delete', delete, name='delete'),
    path('records/<int:pk>/meals/', meals, name='meals'),
    path('records/<int:pk>/meals/create', meals_create, name='meals.create'),
    path('records/<int:pk>/meals/<int:meal_id>/', meals_details, name='meals.details'),
    path('records/<int:pk>/meals/<int:meal_id>/delete', meals_delete, name='meals.delete'),
    path('records/<int:pk>/meals/<int:meal_id>/reload/<int:ingredient_id>', meals_reload, name='meals.reload')
]