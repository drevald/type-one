import requests
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from . import forms

def list(request):
    list = models.Ingredient.objects.all()
    template = 'ingredients.html'
    context = {'list':list}
    return render(request, template, context)

def create(request):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('ingredients:list'))
    ingredient = models.Ingredient()
    form = forms.IngredientForm(request.POST or None, instance=ingredient)
    if form.is_valid():
        print(form.instance.id)
        form.save()
        return HttpResponseRedirect(reverse('ingredients:list'))
    context = {"form":form}
    template = "ingredient.html"
    return render(request, template, context)

def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('ingredients:list'))
    ingredient = models.Ingredient.objects.get(id=pk)
    units = models.IngredientUnit.objects.filter(ingredient=ingredient)
    form = forms.IngredientForm(request.POST or None, instance=ingredient)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:list'))
    context = {"form":form,"units":units,"pk":pk}
    template = "ingredient.html"
    return render(request, template, context)

def delete(request, pk):
    ingredient = Ingredient.objects.get(id=pk)
    ingredient.delete()
    return HttpResponseRedirect(reverse('ingredients:list'))

def unit_add(request, pk):
    unit = models.IngredientUnit(ingredient=models.Ingredient.objects.get(id=pk))
    form = forms.IngredientUnitForm(request.POST or None, instance=unit)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))
    context = {"form":form,"pk":pk}
    template = "unit_add.html"
    return render(request, template, context)

def ingredient_unit_details(request, pk, unit_id):
    unit = models.IngredientUnit.objects.get(id=unit_id)
    form = forms.IngredientUnitForm(request.POST or None, instance=unit)
    print(str(unit))
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))
    context = {"form":form,"pk":pk,"unit_id":unit_id}
    template = "unit_add.html"
    return render(request, template, context)

def ingredient_unit_delete(request, pk, unit_id):
    unit = models.IngredientUnit.objects.get(id=unit_id)
    unit.delete()
    return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))

def units(request):
    units = models.WeightUnit.objects.all()
    template = "units.html"
    context = {"units":units}
    return render(request, template, context)

def unit_create(request):
    unit = models.WeightUnit()
    form = forms.WeightUnitForm(request.POST or None, instance=unit)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:units'))
    return render(request, "unit.html", {"form":form})

def unit_details(request, unit_id):
    unit = models.WeightUnit.objects.get(id=unit_id)
    #unit = models.WeightUnit()
    form = forms.WeightUnitForm(request.POST or None, instance=unit)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:units'))
    return render(request, "unit.html", {"form":form})

def unit_delete(request, unit_id):
    unit = models.WeightUnit.objects.filter(id=unit_id)
    unit.delete()
    return HttpResponseRedirect(reverse('ingredients:units'))


def fetch(request):
    string = request.POST.get('name')
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search?query=' + str(string) + '&api_key=IfJaYBICN1pUVdbsf7u9u1LaKYrYBKS5mqCqFCz7&dataType=SR%20Legacy'
    # 168191
    r = requests.get(url, params=request.GET)
    if r.status_code == 200:
        data = json.loads(r.text)
        print("--------------------")
        print(url)
        print("--------------------")
        records = data["foods"]
        for record in records:
            print(str(record["fdcId"]) + " " + record["description"])    
        context = {"string":string,"records":records}
        return render(request, "fetch.html", context)    
    context = {"string":string}
    return render(request, "fetch.html", context)