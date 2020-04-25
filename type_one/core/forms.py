from django import forms

class RecordForm(forms.Form):
    sugar = forms.CharField()
    insulin = forms.CharField()    
    meal = forms.HiddenInput()
    notes = forms.TextInput()