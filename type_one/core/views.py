from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import FormView
from datetime import datetime
from django import forms 
from .models import SugarLevel, Insulin, Record, SugarLevelUnit, InsulinShot, User
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
        user = User(self.request.user)
        insulinShot = InsulinShot(
            amount_units = form.cleaned_data['insulin'],
            insulin = user.rapid_acting_insulin
        )
        insulinShot.save()
        sugarLevel = SugarLevel(
            value = form.cleaned_data['sugar'], 
            sugarUnit = user.sugar_level_unit
        )
        sugarLevel.save()
        record = Record.objects.create(
            time = datetime.now(), 
            sugarLevel = sugarLevel,
            insulinShot = insulinShot
        )
        return super().form_valid(form)

    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # time = models.TimeField()
    # sugarLevel = models.ForeignKey(SugarLevel, on_delete = models.DO_NOTHING, null=True)
    # insulinShot = models.ForeignKey(InsulinShot, on_delete = models.DO_NOTHING, null=True)
    # meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING, null=True)
    # activityPeriod = models.ForeignKey(ActivityPeriod, on_delete = models.DO_NOTHING, null=True)
    # notes = models.CharField(max_length = 1000, null=True)