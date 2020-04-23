from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import FormView
from django import forms 
from .models import SugarLevel, Insulin, Record, SugarLevelUnit
from .forms import *

class Home(TemplateView):
    template_name = 'index.html'

class Spisok(ListView):
    template_name = 'spisok.html'
    model = Insulin

class Records(ListView):    
    template_name = 'records.html'
    model = Record

class RecordCreate(FormView):
    template_name = 'record_create.html'
    success_url = '/'
    form_class = RecordForm
    model = Record
    fields = '__all__'    
    def form_valid (self, form):
        sugar_level = SugarLevel(1, 1)
        sugar_level.save()
        #sugar = Sugar()
        #sugar.save()
        #sugar = SugarLevel.objects.create(value=form.cleaned_data['sugar'])
        #shot = InsulinShot.objects.create(Insulin.objects.get(0), form.cleaned_data['insulin'])
        #record = Record.object.create()
        return super().form_valid(form)