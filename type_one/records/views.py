from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from datetime import datetime
from ..core.models import User, GlucoseUnit, Insulin
from ..ingredients.models import Ingredient, IngredientUnit
from .models import Record, Meal
from .forms import LongForm, RecordForm, MealIngredientForm

def records(request):
    records_list = Record.objects.all()
    template = loader.get_template('records_list.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

def delete(request, pk):
    record = Record.objects.get(id = pk)
    record.delete()
    return HttpResponseRedirect(reverse('records:list'))

def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record.objects.get(id=pk)
    return store(request, record)

def create(request, type=0):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record(glucose_level_unit = request.user.glucose_level_unit, type=type)
    record.insulin = request.user.rapid_acting_insulin if type==0 else request.user.long_acting_insulin
    return store(request, record)

def store(request, record):
    print(record.type)
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    form = RecordForm(request.POST or None) if record.type == 0 else LongForm(request.POST or None)
    form.instance = record
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('records:list'))
    context = {"form": form}
    return render(request, template, context)

def meals(request, pk):
    meals = Meal.objects.all()
    template = 'meals.html'
    context = {'meals' : meals, 'pk' : pk}
    return render(request, template, context)

def meals_create(request, pk):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('meals', pk))    
    meal = Meal()
    template = 'meal_new.html'
    form = MealIngredientForm(request.POST or None, instance=meal)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('meals', pk))
    context = {"form": form}
    return render(request, template, context)

def meals_details(request, pk, meal_id):    
    return HttpResponse("meal details")

def meals_delete(request, pk, meal_id):    
    return HttpResponse("meal delete")    

def meals_reload(request, pk, meal_id, ingredient_id):    
    return HttpResponse("meal reload")    