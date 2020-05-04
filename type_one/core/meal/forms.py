from django import forms
from type_one.core.models import MealIngredient

class MealIngredientForm (forms.ModelForm):
    class Meta:
        model = MealIngredient
        fields = '__all__'
