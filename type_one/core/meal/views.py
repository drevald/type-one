from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from type_one.core.models import MealIngredient
from .forms import MealIngredientForm

def list(request, pk):
    meals = MealIngredient.objects.all()
    template = 'meals.html'
    context = {'meals' : meals}
    return render(request, template, context)

def create(request, pk):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('meals'))    
    mealingredient = MealIngredient()
    template = 'meal_new.html'
    form = MealIngredientForm(request.POST or None, instance=mealingredient)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('meals'))
    context = {"form": form}
    return render(request, template, context)    