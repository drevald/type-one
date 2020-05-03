from django import forms
from .models import MealIngredient, Record

class MealIngredientForm (forms.ModelForm):
    class Meta:
        model = MealIngredient
        fields = '__all__'

class LongForm (forms.ModelForm):
    insulin_amount = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control input-sm'}), required=False)
    class Meta:
        model = Record
        fields = ['insulin_amount','notes']