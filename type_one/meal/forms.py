from django import forms
from .models import Meal, Ingredient

class MealIngredientForm (forms.ModelForm):
    ingredient = forms.Select()
    class Meta:
        model = Meal
        fields = '__all__'