from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import Record, Insulin, MealIngredient, IngredientUnit, Ingredient, WeightUnit
from .forms import MealIngredientForm, LongForm, RecordForm
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
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    form = RecordForm(request.POST or None, instance=record) if record.type == 0 else LongForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('list'))
    context = {"form": form}
    return render(request, template, context)

def create(request, type=0):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))    
    template = 'record_new.html'
    record = Record(time = datetime.now(), insulin = request.user.rapid_acting_insulin, glucose_level_unit = request.user.glucose_level_unit)
    if (type == 1):
        template = 'record_long.html'
        record.insulin = request.user.long_acting_insulin
        record.type = 1
    form = RecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('list'))
    context = {"form": form}
    return render(request, template, context)