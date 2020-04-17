from django.urls import path
from .views import Home
from .views import Spisok

urlpatterns = [
    path('', Home.as_view()),
    path('spisok/', Spisok.as_view()),
]





