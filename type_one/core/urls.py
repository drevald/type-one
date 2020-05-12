from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'core'

urlpatterns = [
    path('login/',  views.signin, name='signin'),
    path('logout/',  views.signout, name='signout'),
] 