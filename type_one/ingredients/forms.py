from django.utils.translation import gettext as _
from django import forms
from . import models

def get_choices():
    units = models.WeightUnit.objects.all()
    return [(unit.id, _(unit.name)) for unit in units]

def get_iunits():
    iunits = models.IngredientUnit.objects.all()
    return [(iunit.id, _(iunit.ingredient.name)+', '+_(iunit.unit.name)) for iunit in iunits]

class CookedForm(forms.Form):
    unit = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control input-sm col-sm-2'}), label=_("Unit"))
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm col-sm-2'}), label=_("Quantity"), initial=1)
    def __init__(self, *args, **kwargs):
        super(CookedForm, self).__init__(*args, **kwargs)
        self.fields['unit'] = forms.ChoiceField(choices=get_iunits(), widget=forms.Select(attrs={'class' : 'form-control input-sm col-sm-2'}), label=_("Unit"))        

class CookForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm col-sm-4'}))
    class Meta:
        model = models.Ingredient
        fields = ['name']

class WeightUnitForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm col-sm-4'}), label=_("Name"))
    class Meta:
        model = models.WeightUnit
        fields = ['name']

class IngredientUnitForm(forms.Form):
    unit = forms.ChoiceField(widget=forms.Select())
    grams_in_unit = forms.FloatField(widget=forms.NumberInput())
    def __init__(self, *args, **kwargs):
        super(IngredientUnitForm, self).__init__(*args, **kwargs)
        self.fields['unit'] = forms.ChoiceField(choices=get_choices())        
    
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

