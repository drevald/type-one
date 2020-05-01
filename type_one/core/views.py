from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import Record, Insulin, MealIngredient, IngredientUnit, Ingredient 
from datetime import datetime

def records_list(request):
    records_list = Record.objects.all()
    print(records_list)
    template = loader.get_template('records_list.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

def record_new(request):
    record = Record()
    template = loader.get_template('record_new.html')
    context = {'record' : Record(), 'insulins':Insulin.objects.all()}
    return HttpResponse(template.render(context, request))

def record_create(request):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))
    id = request.POST['id']
    record = Record.objects.get(id=id) if id else Record()   
    record.time = datetime.now()
    record.glucose_level =  request.POST['glucose_level']
    record.glucose_level_unit = request.user.glucose_level_unit
    record.insulin_amount = request.POST['insulin_amount']
    record.insulin = request.user.rapid_acting_insulin
    record.notes = request.POST.get('notes')
    record.save()    
    return HttpResponseRedirect(reverse('list'))

def record_delete(request, pk):
    record = Record.objects.get(id = pk)
    record.delete()
    return HttpResponseRedirect(reverse('list'))

def record_update(request, pk):
    record = Record.objects.get(id = pk)
    template = loader.get_template('record_new.html')
    context = {'record' : record, 'insulins':Insulin.objects.all()}
    return HttpResponse(template.render(context, request))

def meal(request, pk = None):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))    
    template = loader.get_template('meal.html')
    context = {'A':'B'}
    return HttpResponse(template.render(context, request))

def meal_add(request):
    if 'meal_ingredients' not in request.session:
        meal_ingredients = []
    else:
        meal_ingredients = request.session['meal_ingredients']
    meal_ingredient = MealIngredient(
        ingredient = Ingredient.objects.first(),
        ingredient_unit = IngredientUnit.objects.first(),
        quantity = 0
    )
    print(meal_ingredient)
    meal_ingredients.clear
    meal_ingredients.append(meal_ingredient)
    request.session['meal_ingredients'] = meal_ingredients
    return render(request = request, template_name = 'meal.html')

def meal_delete(request, pk):
    del request.session['meal_ingredients'][pk-1]
    return HttpResponseRedirect(reverse('meal'))

def meal_update(request, pk):
    return HttpResponseRedirect(reverse('meal'))
