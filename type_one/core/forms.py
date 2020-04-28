from django import forms
from .models import Ingredient

class RecordForm(forms.Form):
    sugar = forms.CharField()
    insulin = forms.CharField()    
    meal = forms.HiddenInput()
    notes = forms.TextInput()

class MealIngredientForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all())
