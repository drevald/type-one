from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', records_list, name="list"),
    path('create/', record_create, name="create"),
    path('new/', record_new, name="new"),
    path('update/<int:pk>', record_update, name="update"),
    path('delete/<int:pk>', record_delete, name="delete"),
    path('meal/<int:pk>', meal, name="meal"),
    path('meal', meal, name="meal"),
    path('meal/new', meal_new, name="meal.new"),
    path('meal/update/store/', meal_update_store, name="meal.update.store"),
    path('meal/update/<int:pk>', meal_update, name="meal.update"),
    path('meal/delete/<int:pk>', meal_delete, name="meal.delete"),


]


