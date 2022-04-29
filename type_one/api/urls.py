from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from type_one.api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/', views.UserDetails.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('records/', views.RecordsList.as_view(), name='records'),
    path('record/<int:pk>/', views.RecordDetails.as_view()),
    path('record/<int:pk>/photos/', views.PhotoCreate.as_view()),
    path('record/<record_id>/photo/<pk>/', views.PhotoRetrieveUpdateDestroy.as_view()),
    path('record/<int:pk>/meals/', views.MealsList.as_view()),
    path('record/<record_id>/meal/<int:pk>/', views.MealDetails.as_view()),
    path('ingredients/', views.IngredientsList.as_view(), name='ingredients'),
    path('ingredient/<int:pk>/', views.IngredientsDetails.as_view(), name='ingredient'),
    path('ingredient/<int:pk>/hints/', views.IngredientsHintCreate.as_view(), name='hint_add'),
    path('ingredient/<int:pk>/hints/<hint_id>', views.IngredientsHintDelete.as_view(), name='hint_delete'),
]

