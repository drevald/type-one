from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from .models import *

class Home(TemplateView):
    template_name = 'index.html'

class Spisok(ListView):
    template_name = 'spisok.html'
    model = Insulin

class Records(ListView):    
    template_name = 'records.html'
    model = Record

class RecordCreate(CreateView):
    template_name = 'record_create.html'
    model = Record
    fields = '__all__'