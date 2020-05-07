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
    print(record.glucose_level)
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    meals = Meal.objects.filter(record=record.id) if record.id else None
    breads = [meal.ingredient.bread_units_per_100g * meal.quantity * meal.ingredient_unit.grams_in_unit for meal in meals] if meals else None
    meal_details = [str(meal) for meal in meals] if meals else None
    meal_details_str = ','.join(meal_details) if meal_details else None
    record.bread_units = sum(breads)/100 if meals else record.bread_units    
    form = RecordForm(request.POST or None, instance=record) if record.type == 0 else LongForm(request.POST or None, instance=record)        
    print(form)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('records:list'))
    context = {"form": form, "meals":meals, "meal_details":meal_details_str}
    return render(request, template, context)

def meals(request, pk):
    meals = Meal.objects.filter(record=Record.objects.get(id=pk))
    template = 'meals.html'
    context = {'meals' : meals, 'pk' : pk}
    return render(request, template, context)

def meals_create(request, pk, ingredient_id=None):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))
    sel_ingr = Ingredient.objects.get(id=ingredient_id) if ingredient_id else Ingredient.objects.first()
    meal = Meal(
        record = Record(id=pk), 
        ingredient=sel_ingr,
        ingredient_unit=IngredientUnit.objects.filter(ingredient=sel_ingr).first()
    )    
    template = 'meal_new.html'
    form = MealIngredientForm(pk, request.POST or None, instance=meal)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))
    context = {"form": form}
    return render(request, template, context)

def meals_details(request, pk, meal_id):    
    meal = Meal.objects.get(id=meal_id)
    template = 'meal_new.html'
    form = MealIngredientForm(pk, request.POST or None, instance=meal)
    if form.is_valid():
        print(form.instance.ingredient)
        print(form.instance.ingredient_unit)
        form.save()
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))
    context = {"form": form}
    return render(request, template, context)

def meals_delete(request, pk, meal_id):  
    meal = Meal.objects.get(id=meal_id) 
    meal.delete()
    return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))

def meals_reload_new(request, pk, ingredient_id):
    meal = Meal(
        record = Record(id=pk), 
        ingredient=Ingredient.objects.get(id=ingredient_id),
        ingredient_unit=IngredientUnit.objects.filter(ingredient=Ingredient.objects.get(id=ingredient_id)).first(),        
    )
    template = 'meal_new.html'
    form = MealIngredientForm(request.POST or None, instance=meal)
    print(form.instance.ingredient_unit)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))
    context = {"form": form}
    return HttpResponseRedirect(reverse('records:meals_create', kwargs={'pk':pk, 'ingredient_id':ingredient_id}))

def meals_reload(request, pk, meal_id, ingredient_id):    
    meal = Meal.objects.get(id=meal_id)
    meal.ingredient = Ingredient.objects.get(id=ingredient_id)
    meal.ingredient_unit = IngredientUnit.objects.filter(ingredient=Ingredient.objects.get(id=ingredient_id)).first()
    meal.save()
    return HttpResponseRedirect(reverse('records:meals_details', kwargs={'pk':pk, 'meal_id':meal.id}))

