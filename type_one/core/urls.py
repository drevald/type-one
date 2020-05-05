from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.records, name='list'),
    path('create/<int:type>', views.create, name='create'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('<int:pk>/meals/', views.meals, name='meals'),
    path('<int:pk>/meals/create', views.meals_create, name='meals.create'),
    path('<int:pk>/meals/<int:meal_id>/', views.meals_details, name='meals.details'),
    path('<int:pk>/meals/<int:meal_id>/delete', views.meals_delete, name='meals.delete'),
    path('<int:pk>/meals/<int:meal_id>/reload/<int:ingredient_id>', views.meals_reload, name='meals.reload')
]