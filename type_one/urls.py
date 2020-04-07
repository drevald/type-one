from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    url('accounts/', include('allauth.urls')),
]