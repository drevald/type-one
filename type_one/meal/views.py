from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Meal
from .forms import MealIngredientForm

def list(request, pk):
    meals = Meal.objects.all()
    template = 'meals.html'
    context = {'meals' : meals}
    return render(request, template, context)

def create(request, pk):    
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