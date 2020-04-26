from django import forms

class RecordForm(forms.Form):

    #sugar = forms.CharField(label='Sugar', widget=forms.NumberInput(attrs={'id':'sugar','class':'form-control'}))
    sugar = forms.CharField()
    insulin = forms.CharField()    
    meal = forms.HiddenInput()
    notes = forms.TextInput()