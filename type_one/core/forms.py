from django import forms
from .models import MealIngredient

class MealIngredientForm (forms.ModelForm):
    class Meta:
        model = MealIngredient
        fields = '__all__'

class RecordForm (forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'