from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import FormView
from datetime import datetime
from django import forms 
from .models import SugarLevel, Insulin, Record, SugarLevelUnit, InsulinShot, User
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(TemplateView):
    template_name = 'index.html'

class Spisok(ListView):
    template_name = 'spisok.html'
    model = Insulin

class Records(ListView):    
    template_name = 'records.html'
    model = Record

class RecordCreate(LoginRequiredMixin, FormView):
    template_name = 'record_create.html'
    success_url = '/'
    form_class = RecordForm
    model = Record
    fields = '__all__'    
    def form_valid (self, form):
        #user = User(self.request.user)
        sugarLevel = SugarLevel(
            value = form.cleaned_data['sugar'], 
            sugarUnit = self.request.user.sugar_level_unit)
        sugarLevel.save()
        insulinShot = InsulinShot(
            amount_units = form.cleaned_data['insulin'],
            insulin = self.request.user.rapid_acting_insulin
        )
        insulinShot.save()
        record = Record.objects.create(
            time = datetime.now(), 
            sugarLevel = sugarLevel,
            insulinShot = insulinShot
        )
        return super().form_valid(form)

