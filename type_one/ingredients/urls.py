from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'ingredients'

urlpatterns = [
    path('', views.all, name='list'),
    path('<str:ch>/', views.letter, name='letter'),
    path('create/', views.create, name='create'),
    path('fetch/', views.fetch, name='fetch'),
    path('fetch/<int:id>/select/<str:type>', views.fetch_select, name='fetch_select'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/units/add', views.unit_add, name='unit_add'),
    path('<int:pk>/units/<int:unit_id>', views.ingredient_unit_details, name='ingredient_unit_details'),
    path('<int:pk>/units/<int:unit_id>/delete', views.ingredient_unit_delete, name='ingredient_unit_delete'),
    path('<int:pk>/hints/add', views.hints_add, name='hint_add'),
    path('<int:pk>/hints/<int:hint_id>', views.ingredient_hint_details, name='ingredient_hint_details'),
    path('<int:pk>/hints/<int:hint_id>/delete', views.ingredient_hint_delete, name='ingredient_hint_delete'),
    path('units/', views.units, name='units'),
    path('units/new', views.unit_create, name='unit_create'),
    path('units/<int:unit_id>/', views.unit_details, name='unit_details'),
    path('units/<int:unit_id>/delete', views.unit_delete, name='unit_delete'),
    path('cook/', views.cook, name='cook'),
    path('cook/add', views.cooked_add, name='cooked_add'),
    path('cook/<int:id>', views.cooked_details, name='cooked_details'),
    path('cook/<int:id>/delete', views.cooked_delete, name='cooked_delete'),
    path('types/', views.types, name='types'),
    path('types/add', views.type_add, name='type_create'),
    path('types/<int:type_id>/', views.type_details, name='type_details'),
    path('types/<int:type_id>/delete', views.type_delete, name='type_delete'),
]
