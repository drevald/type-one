from django.urls import path
from .views import Home
from .views import *

urlpatterns = [
    path('', Records.as_view()),
    path('create/', RecordCreate.as_view()),
    path('spisok/', Spisok.as_view()),

]
