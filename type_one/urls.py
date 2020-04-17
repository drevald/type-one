from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    url('accounts/', include('allauth.urls')),
    path('', include('type_one.core.urls')),
    path('admin/', admin.site.urls)
]
