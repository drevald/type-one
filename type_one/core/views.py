from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import Record, Insulin, MealIngredient, IngredientUnit, Ingredient, WeightUnit
from .forms import LongForm, RecordForm
from datetime import datetime

def list(request):
    records_list = Record.objects.all()
    template = loader.get_template('records_list.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

def delete(request, pk):
    record = Record.objects.get(id = pk)
    record.delete()
    return HttpResponseRedirect(reverse('list'))

def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))    
    record = Record.objects.get(id=pk)
    return store(request, record)

def create(request, type=0):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))    
    record = Record(glucose_level_unit = request.user.glucose_level_unit)
    record.insulin = request.user.rapid_acting_insulin if type==0 else request.user.long_acting_insulin
    return store(request, record)

def store(request, record):
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    form = RecordForm(request.POST or None) if record.type == 0 else LongForm(request.POST or None)
    form.instance = record
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('list'))
    context = {"form": form}
    return render(request, template, context)
