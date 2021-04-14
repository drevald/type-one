from django.utils.translation import gettext as _
from django import forms
from .models import Record, Meal, Ingredient, IngredientUnit, Photo

class MealForm (forms.ModelForm):    
    ingredient_unit = forms.ModelChoiceField(queryset=IngredientUnit.objects.all(), widget=forms.Select(attrs={'class' : 'form-control input-sm'}))    
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}))
    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.fields['ingredient_unit'] = forms.ChoiceField(choices=[ (o.id, _(str(o.ingredient.name)) + ',  ' + _(str(o.unit.name))) for o in IngredientUnit.objects.all()])
    class Meta:
        model = Meal
        fields = ['ingredient_unit','quantity']

class LongForm (forms.ModelForm):
    insulin_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control input-sm'}), required=False)
    class Meta:
        model = Record
        fields = ['insulin_amount','notes']

class RecordForm (forms.ModelForm):
    insulin_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0, required=False)
    glucose_level = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0, required=False)
    bread_units = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control input-sm'}), initial=0, required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control input-sm'}), required=False)
    class Meta:
        model = Record
        fields = ['insulin_amount','glucose_level','bread_units','notes']

class UploadFileForm(forms.Form):
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'onchange':'preview(this.form)','capture':'camera','class':'form-control-file'}))    
    class Meta:
        model = Photo
        fileds = ['data']