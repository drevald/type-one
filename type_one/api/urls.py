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
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('records/', views.RecordsList.as_view(), name='records'),
    path('record/<int:pk>/', views.RecordDetails.as_view()),
    path('record/<int:pk>/photos/', views.PhotoCreate.as_view()),
    path('record/<record_id>/photo/<pk>/', views.PhotoRetrieveUpdateDestroy.as_view()),
    path('record/<int:pk>/meals/', views.MealsList.as_view()),
    path('ingredients/', views.IngredientsList.as_view(), name='ingredients')
]

