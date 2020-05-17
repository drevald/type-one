from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from datetime import datetime
from ..core.models import User, GlucoseUnit, Insulin
from ..ingredients.models import Ingredient, IngredientUnit
from .models import Record, Meal
from .forms import MealForm, RecordForm, LongForm

@login_required
def default(request):
    records_list = Record.objects.filter(user=request.user)
    template = loader.get_template('records.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

@login_required
def records(request):
    records_list = Record.objects.filter(user=request.user)
    template = loader.get_template('records.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

@login_required
def delete(request, pk):
    record = Record.objects.get(id = pk,user=request.user)
    record.delete()
    return HttpResponseRedirect(reverse('records:list'))

@login_required
def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record.objects.get(id=pk,user=request.user)    
    return store(request, record)

@login_required
def create(request, type=0):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record(glucose_level_unit = request.user.glucose_level_unit, type=type,user=request.user)
    record.insulin = request.user.rapid_acting_insulin if type==0 else request.user.long_acting_insulin
    return store(request, record)

@login_required
def store(request, record):
    print(record.glucose_level)
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    meals = Meal.objects.filter(record=record.id) if record.id else None
    meal_details = [str(meal) for meal in meals] if meals else None
    meal_details_str = ','.join(meal_details) if meal_details else None
    breads = [meal.quantity * meal.ingredient_unit.grams_in_unit * meal.ingredient_unit.ingredient.bread_units_per_100g for meal in meals] if meals else None
    record.bread_units = sum(breads)/100 if meals else record.bread_units    
    form = RecordForm(request.POST or None, instance=record) if record.type == 0 else LongForm(request.POST or None, instance=record)        
    print(form)
    if form.is_valid():
        form.save()
        print("Returning to " + reverse('records:list'))
        return HttpResponseRedirect(reverse('records:list'))
    context = {"form": form, "meals":meals, "meal_details":meal_details_str}
    return render(request, template, context)

@login_required
def meals(request, pk):
    meals = Meal.objects.filter(record=Record.objects.get(id=pk),user=request.user)
    template = 'meals.html'
    context = {'meals' : meals, 'pk' : pk}
    return render(request, template, context)

@login_required
def meals_create(request, pk):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))        
    meal = Meal(record=Record.objects.get(id=pk), ingredient_unit=IngredientUnit.objects.first(),user=request.user)
    form = MealForm(request.POST or None, instance=meal)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))
    template = 'meal_new.html'
    context = {'form':form}
    return render(request, template, context)

@login_required
def meals_details(request, pk, meal_id):   
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))        
    meal = Meal.objects.get(id=meal_id,user=request.user)    
    form = MealForm(request.POST or None, instance=meal)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))
    template = 'meal_new.html'
    return render(request, template, {'form':form})

@login_required
def meals_delete(request, pk, meal_id):  
    meal = Meal.objects.get(id = meal_id,user=request.user)
    meal.delete()
    return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))

@login_required
def recent(request, pk):    
    list = Record.objects.exclude(id=pk,user=request.user)
    template = "meals_recent.html"
    context = {'pk':pk,'list':list}
    return render(request, template, context) 

@login_required
def select(request, pk, record_id):   
    print(record_id)
    meals = Record.objects.get(id=record_id,user=request.user).meals.filter(user=request.user)
    record = Record.objects.get(id=pk)
    for meal in meals:
        imported_meal = Meal(
            ingredient_unit=meal.ingredient_unit, 
            quantity=meal.quantity,
            record=record)
        imported_meal.save()
        print(imported_meal)
    return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))
