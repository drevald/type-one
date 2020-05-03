from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import Record, Insulin, MealIngredient, IngredientUnit, Ingredient, WeightUnit
from .forms import MealIngredientForm
from datetime import datetime

def records_list(request):
    records_list = Record.objects.all()
    print(records_list)
    template = loader.get_template('records_list.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

def record_create(request):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))
    id = request.POST.get('id', None)
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

def record_new(request):
    record = Record()
    template = loader.get_template('record_new.html')
    context = {'record' : Record(), 'insulins':Insulin.objects.all()}
    return HttpResponse(template.render(context, request))

def meal(request, pk = None):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('list'))    
    template = loader.get_template('meal.html')
    request.session['record_id'] = pk
    context = {'A':'B'}
    return HttpResponse(template.render(context, request))

def meal_update_store(request):
    if 'meal_ingredients' not in request.session:
        meal_ingredients = []
    else:
        meal_ingredients = request.session['meal_ingredients']
    pk = request.POST.get('pk', None)
    ingredient = request.session['meal_ingredients'][int(pk)-1] if pk else MealIngredient()
    ingredient.ingredient = Ingredient.objects.get(id=int(request.POST.get('ingredient_id')))
    ingredient.ingredient_unit = IngredientUnit.objects.get(id=int(request.POST.get('unit_id')))
    ingredient.quantity = request.POST.get('quantity')
    meal_ingredients.clear
    if pk:
        meal_ingredients[int(pk)-1] = ingredient
    else: 
        meal_ingredients.append(ingredient)
    return render(request = request, template_name = 'meal.html')

def meal_delete(request, pk):
    del request.session['meal_ingredients'][pk-1]
    return HttpResponseRedirect(reverse('meal'))

def meal_update(request, pk=None):
    template = loader.get_template('meal_ingredient.html')
    meal_ingredient = request.session['meal_ingredients'][pk-1]
    units = IngredientUnit.objects.filter(ingredient = Ingredient.objects.first())
    ingredients = Ingredient.objects.all
    context = {'meal_ingredient':meal_ingredient, 'ingredients':ingredients, 'units':units, 'pk':pk}
    return HttpResponse(template.render(context, request))    

def meal_update_reload(request, pk=None, sel=None):
    template = loader.get_template('meal_ingredient.html')
    meal_ingredient = request.session['meal_ingredients'][pk-1]
    meal_ingredient.ingredient = Ingredient.objects.get(id=sel)
    units = IngredientUnit.objects.filter(ingredient = meal_ingredient.ingredient)
    ingredients = Ingredient.objects.all
    context = {'meal_ingredient':meal_ingredient, 'ingredients':ingredients, 'units':units, 'pk':pk}
    return HttpResponse(template.render(context, request))   

def meal_new(request):    
    template = loader.get_template('meal_ingredient.html')
    meal_ingredient = MealIngredient()
    meal_ingredient.ingredient = Ingredient.objects.first()
    meal_ingredient.ingredient_unit = IngredientUnit.objects.filter(ingredient = meal_ingredient.ingredient).first()
    units = IngredientUnit.objects.filter(ingredient = Ingredient.objects.first())
    ingredients = Ingredient.objects.all
    context = {'meal_ingredient':meal_ingredient, 'ingredients':ingredients, 'units':units}
    return HttpResponse(template.render(context, request)) 

def meal_save(request):
    if 'record_id' not in request.session:
        return HttpResponseRedirect(reverse('new'))
    else:
        return HttpResponseRedirect(reverse('new'))
