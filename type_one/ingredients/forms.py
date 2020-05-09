from django import forms
from . import models

class IngredientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-sm'}))
    bread_units_per_100g  = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    glycemic_index = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), required=False)
    fat_per_100g = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    carbohydrate_per_100g = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    protein_per_100g = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    energy_kKkal_per_100g = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    class Meta:
        model = models.Ingredient
        fields = [
            'name',
            'bread_units_per_100g',
            'glycemic_index',
            'fat_per_100g',
            'carbohydrate_per_100g',
            'protein_per_100g',
            'energy_kKkal_per_100g'
        ]

