import sys
import os
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

def hello(request):
    return HttpResponse('Hello World')

urlpatterns = [
path('', hello)
]

SECRET_KEY = 'key'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "type_one.settings")
execute_from_command_line(sys.argv)