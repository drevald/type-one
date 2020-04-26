from .models import SugarLevel, Insulin, Record, SugarLevelUnit, InsulinShot, User, Meal, MealIngredient
from .forms import *
from django.views.generic import TemplateView, ListView, CreateView, FormView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from datetime import datetime
from django import forms 
from django.urls import reverse_lazy

class Home(TemplateView):
    template_name = 'index.html'

class Spisok(ListView):
    template_name = 'spisok.html'
    model = Insulin

class Records(LoginRequiredMixin, ListView):    
    template_name = 'records.html'
    model = Record

class RecordDeleteView(LoginRequiredMixin, DeleteView):    
    model = Record
    template_name = 'record_delete.html'
    success_url = '/'

class RecordUpdateView(LoginRequiredMixin, UpdateView):    
    model = Record
    template_name = 'record_update.html'
    success_url = '/'
    fields = '__all__'    

class RecordCreate(LoginRequiredMixin, FormView):
    template_name = 'record_create.html'
    success_url = '/'
    form_class = RecordForm
    model = Record
    fields = '__all__'    
    def form_valid (self, form):
        insulinShot = InsulinShot(
            amount_units = form.cleaned_data['insulin'],
            insulin = self.request.user.rapid_acting_insulin
        )
        insulinShot.save()
        sugarLevel = SugarLevel(
            value = form.cleaned_data['sugar'], 
            sugar_unit = self.request.user.sugar_level_unit
        )
        sugarLevel.save()
        record = Record.objects.create(
            time = datetime.now(), 
            sugar_level = sugarLevel,
            insulin_shot = insulinShot
        )
        return super().form_valid(form)

class MealUpdateView (LoginRequiredMixin, TemplateView): 
    model = Meal
    template_name = 'meal_update.html'
    success_url = '/'

class MealIngredientCreateView (LoginRequiredMixin, TemplateView): 
    model = MealIngredient
    template_name = 'meal_update.html'
    success_url = '/'

def mealupdate(request):
    return render(request, 'meal_update.html');

def mealingredientadd(request):
    return render(request, 'meal_update.html');
