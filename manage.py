import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

settings.configure(ROOT_URLCONF=__name__, ALLOWED_HOSTS='*')

def hello(request):
    return HttpResponse('Hello World')

urlpatterns = [
path('', hello)
]

execute_from_command_line(sys.argv)