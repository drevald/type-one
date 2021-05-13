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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('records/', views.RecordsList.as_view()),
    path('record/<int:pk>/', views.RecordDetails.as_view()),
    path('record/create/', views.RecordCreate.as_view()),
    path('record/<int:pk>/update', views.RecordUpdate.as_view()),
    path('insulins/', views.InsulinsList.as_view()),
]

