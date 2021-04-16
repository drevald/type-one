from django.utils.translation import gettext as _
from django import forms
from . import models

def get_choices():
    units = models.WeightUnit.objects.all()
    return [(unit.id, _(unit.name)) for unit in units]

class CookedForm(forms.Form):
    unit = forms.ModelChoiceField(queryset=models.IngredientUnit.objects.all(), widget=forms.Select(attrs={'class' : 'form-control input-sm col-sm-2'}))
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm col-sm-2'}))
    class Meta:
        fields = ['unit', 'quantity']

class CookForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm col-sm-4'}))
    class Meta:
        model = models.Ingredient
        fields = ['name']

class WeightUnitForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm col-sm-4'}))
    class Meta:
        model = models.WeightUnit
        fields = ['name']

class IngredientUnitForm(forms.Form):
    unit = forms.ChoiceField(widget=forms.Select())
    grams_in_unit = forms.FloatField(widget=forms.NumberInput())
    def __init__(self, *args, **kwargs):
        super(IngredientUnitForm, self).__init__(*args, **kwargs)
        self.fields['unit'] = forms.ChoiceField(choices=get_choices())        
    class Meta:
        model = models.IngredientUnit
        fields = ['unit','grams_in_unit']
    
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

