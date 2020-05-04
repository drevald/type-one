from django import forms
from type_one.core.models import Meal, Ingredient

class MealIngredientForm (forms.ModelForm):
    ingredient = forms.Select()
    class Meta:
        model = Meal
        fields = '__all__'