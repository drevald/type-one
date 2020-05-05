from django import forms
from .models import Record, Meal, Ingredient, IngredientUnit

class MealIngredientForm (forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        label='Ingredient', 
        queryset=Ingredient.objects.all(), 
        widget=forms.Select(attrs={'class' : 'form-control input-sm'})
    )
    ingredient_unit = forms.ModelChoiceField(
        label='Unit', 
        queryset=IngredientUnit.objects.filter(ingredient=2), 
        widget=forms.Select(attrs={'class' : 'form-control input-sm'})
    )
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    class Meta:
        model = Meal
        fields = ['ingredient', 'ingredient_unit', 'quantity']

class LongForm (forms.ModelForm):
    insulin_amount = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control input-sm'}), required=False)
    class Meta:
        model = Record
        fields = ['insulin_amount','notes']

class RecordForm (forms.ModelForm):
    insulin_amount = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0, required=False)
    glucose_level = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0, required=False)
    bread_units = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0, required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control input-sm'}), required=False)
    class Meta:
        model = Record
        fields = ['insulin_amount', 'glucose_level', 'bread_units', 'notes']