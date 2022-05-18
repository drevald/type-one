from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from type_one.records.views import handle_uploaded_file
import requests
import json
from . import models
from . import forms
from bs4 import BeautifulSoup

@login_required
def all(request):
    #ls = list(models.Ingredient.objects.filter(Q(user=request.user)|Q(user__isnull=True)))
    ls = list(models.Ingredient.objects.all())
    template = "ingredients.html"
    ls.sort(key=lambda x: _(x.name))

    page = request.GET.get('page', 1)
    paginator = Paginator(ls, 10)
    try:
        ingrs = paginator.page(page)
    except PageNotAnInteger:
        ingrs = paginator.page(1)
    except EmptyPage:
        ingrs = paginator.page(paginator.num_pages)    
    
    context = {'list':ingrs}
    return render(request, template, context)

@login_required
def create(request):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('ingredients:list'))
    ingredient = models.Ingredient(user=request.user)
    form = forms.IngredientForm(request.POST or None, instance=ingredient)
    if form.is_valid():
        print(form.instance.id)
        form.save()
        return HttpResponseRedirect(reverse('ingredients:list'))
    context = {"form":form}
    template = "ingredient.html"
    return render(request, template, context)

@login_required
def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('ingredients:list'))
    ingredient = models.Ingredient.objects.get(id=pk)
    units = models.IngredientUnit.objects.filter(ingredient=ingredient)
    hints = models.IngredientHint.objects.filter(ingredient=ingredient)
    form = forms.IngredientForm(request.POST or None, instance=ingredient)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:list'))
    context = {"form":form,"units":units,"hints":hints,"pk":pk}
    template = "ingredient.html"
    return render(request, template, context)

@login_required
def delete(request, pk):
    #ingredient = models.Ingredient.objects.get(id=pk, user=request.user)
    ingredient = models.Ingredient.objects.get(id=pk)
    ingredient.delete()
    return HttpResponseRedirect(reverse('ingredients:list'))

@login_required
def unit_add(request, pk):    
    form = forms.IngredientUnitForm(request.POST or None)
    if form.is_valid():
        unit = models.IngredientUnit(
            ingredient=models.Ingredient.objects.get(id=pk),
            user=request.user,
            unit=models.WeightUnit.objects.get(id=form.data['unit']),
            grams_in_unit= form.data['grams_in_unit']
        )   
        unit.save()     
        return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))
    context = {"form":form,"pk":pk}
    template = "unit_add.html"
    return render(request, template, context)

@login_required
def ingredient_unit_details(request, pk, unit_id):
    #unit = models.IngredientUnit.objects.get(id=unit_id, user=request.user)
    unit = models.IngredientUnit.objects.get(id=unit_id)
    form = forms.IngredientUnitForm(request.POST or None)
    form.fields["name"]="aaa"
    print(str(unit))
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))
    context = {"form":form,"pk":pk,"unit_id":unit_id}
    template = "unit_add.html"
    return render(request, template, context)

@login_required
def ingredient_unit_delete(request, pk, unit_id):
    #unit = models.IngredientUnit.objects.get(id=unit_id, user=request.user)
    unit = models.IngredientUnit.objects.get(id=unit_id)
    unit.delete()
    return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))

@login_required
def units(request):
    # units = models.WeightUnit.objects.filter(user=request.user)
    units = models.WeightUnit.objects.all()
    template = "units.html"
    context = {"units":units}
    return render(request, template, context)

@login_required
def unit_create(request):
    form = forms.WeightUnitForm(request.POST or None)
    if form.is_valid():
        unit = models.WeightUnit(
            name=form.data["name"],
            user=request.user)
        unit.save()
        return HttpResponseRedirect(reverse('ingredients:units'))
    return render(request, "unit.html", {"form":form})

@login_required
def unit_details(request, unit_id):
    unit = models.WeightUnit.objects.get(id=unit_id,user=request.user)
    if request.method == 'POST':
        form = forms.WeightUnitForm(request.POST or None)
        if form.is_valid():
            unit.name=form.data["name"]
            unit.save()
            return HttpResponseRedirect(reverse('ingredients:units'))
    else:
        form = forms.WeightUnitForm(initial={'name':unit.name})           
    return render(request, "unit.html", {"form":form})

@login_required
def unit_delete(request, unit_id):
    unit = models.WeightUnit.objects.filter(id=unit_id,user=request.user)
    unit.delete()
    return HttpResponseRedirect(reverse('ingredients:units'))

@login_required
def fetch(request):
    string = request.POST.get('name')
    r = requests.get("https://calorizator.ru/search/node/" + str(string))
    html_doc = r.text
    soup = BeautifulSoup (html_doc, 'html.parser')
    records = []
    for p in list(soup.find_all('dt')):
        if 'product' not in str(p.a['href']) and 'recept' not in str(p.a['href']):
            continue
        if not (p.a['href'].split('/')[-1]).isdigit():
            continue
        records.append({'description':p.a.string,'id':p.a['href'].split('/')[-1],'type':p.a['href'].split('/')[-2]})
    context = {"string":string,"records":records}
    return render(request, "fetch.html", context)

@login_required
def fetch_select(request, id, type):
    url = 'https://calorizator.ru/' + str(type) + '/' + str(id)
    r = requests.get(url, params=request.GET)    
    html_doc = r.text
    soup = BeautifulSoup (html_doc, 'html.parser')

    ingredient = models.Ingredient(user=request.user)
    ingredient.name = soup.findAll("span", {"itemprop" : "name"})[0].text
    ingredient.energy_kKkal_per_100g = int(float(soup.findAll("span", {"itemprop" : "calories"})[0].text.split(" ")[0].replace(',','.')))
    ingredient.protein_per_100g = int(float(soup.findAll("span", {"itemprop" : "proteinContent"})[0].text.split(" ")[0].replace(',','.')))
    ingredient.fat_per_100g = int(float(soup.findAll("span", {"itemprop" : "fatContent"})[0].text.split(" ")[0].replace(',','.')))
    ingredient.carbohydrate_per_100g = int(float(soup.findAll("span", {"itemprop" : "carbohydrateContent"})[0].text.split(" ")[0].replace(',','.')))
    ingredient.bread_units_per_100g = round(ingredient.carbohydrate_per_100g/12, 1)
    ingredient.glycemic_index = 50

    form = forms.IngredientForm(request.POST or None, instance = ingredient)
    print(form)
    if form.is_valid():
        ingredient = form.instance
        ingredient.save()
        gram_weight_unit = models.WeightUnit.objects.get(id=0)
        ingredient_weight_unit = models.IngredientUnit(unit=gram_weight_unit, ingredient=ingredient, user=request.user, grams_in_unit=1)
        ingredient_weight_unit.save()
        return HttpResponseRedirect(reverse('ingredients:list'))
    context = {"form":form}
    template = "ingredient.html"
    return render(request, template, context)

@login_required
def cook(request):
    ingredient = models.Ingredient(user=request.user)
    form = forms.CookForm(request.POST or None, instance=ingredient)
    if form.is_valid():

        ingredient = models.Ingredient(name=form.cleaned_data["name"], user=request.user)
        ingr_units = [i["ingredient"] for i in request.session['cooked_ingredients']]
        amounts = [i["quantity"] for i in request.session['cooked_ingredients']]
        unit_weights = [i.grams_in_unit for i in ingr_units]
        ingrs = [i.ingredient for i in ingr_units]
        total = sum([x*y for (x, y) in zip (amounts, unit_weights)])
        
        ingredient.carbohydrate_per_100g = sum([x*y*z for (x, y, z) in zip(amounts, unit_weights, [i.carbohydrate_per_100g for i in ingrs])])/total
        ingredient.bread_units_per_100g = round(ingredient.carbohydrate_per_100g/12, 1)
        ingredient.fat_per_100g = sum([x*y*z for (x, y, z) in zip(amounts, unit_weights, [i.fat_per_100g for i in ingrs])])/total
        ingredient.protein_per_100g = sum([x*y*z for (x, y, z) in zip(amounts, unit_weights, [i.protein_per_100g for i in ingrs])])/total
        ingredient.energy_kKkal_per_100g = sum([x*y*z for (x, y, z) in zip(amounts, unit_weights, [i.energy_kKkal_per_100g for i in ingrs])])/total
        ingredient.glycemic_index = sum([x*y*z for (x, y, z) in zip(amounts, unit_weights, [i.glycemic_index for i in ingrs])])/total
        ingredient.save()

        gram_weight_unit = models.WeightUnit.objects.get(id=0)
        ingredient_weight_unit = models.IngredientUnit(unit=gram_weight_unit, ingredient=ingredient, user=request.user, grams_in_unit=1)
        ingredient_weight_unit.save()

        request.session['cooked_ingredients'].clear()
        return HttpResponseRedirect(reverse('ingredients:list'))

    template = "cook.html"
    context = {"form":form}
    return render(request, template, context)

@login_required
def cooked_add(request):
    form = forms.CookedForm(request.POST or None)
    if form.is_valid():
        print()
        if 'cooked_ingredients' not in request.session:
            request.session['cooked_ingredients'] = []
        ingredient = models.IngredientUnit.objects.get(id=form.cleaned_data["unit"])
        cooked_ingredients = request.session['cooked_ingredients']
        cooked_ingredients.append({
            "ingredient":ingredient,
            "quantity":form.cleaned_data["quantity"]
            })
        return HttpResponseRedirect(reverse("ingredients:cook"))            
    template='cooked_add.html'
    context = {'form':form}
    return render(request, template, context)

@login_required
def cooked_details(request, id):
    unit = request.session['cooked_ingredients'][id-1]["ingredient"]
    quantity = request.session['cooked_ingredients'][id-1]["quantity"]
    form = forms.CookedForm(request.POST or None, initial={'unit':unit,'quantity':quantity})
    if form.is_valid():
        print()
        if 'cooked_ingredients' not in request.session:
            request.session['cooked_ingredients'] = []
        cooked_ingredients = request.session['cooked_ingredients']
        cooked_ingredients[id-1] = {
            "ingredient":form.cleaned_data["unit"],
            "quantity":form.cleaned_data["quantity"]
            }
        return HttpResponseRedirect(reverse("ingredients:cook"))            
    template='cooked_add.html'
    context = {'form':form}
    return render(request, template, context)

@login_required
def cooked_delete(request, id):
    request.session['cooked_ingredients'].pop(id-1)
    return HttpResponseRedirect(reverse("ingredients:cook"))

@login_required
def hints_add(request, pk):
    form = forms.UploadHintForm(request.POST or None)
    if form.is_valid():
        ingredient = models.Ingredient.objects.get(id=pk)
        (thumb, data) = handle_uploaded_file(request.FILES['file'])
        hint = models.IngredientHint(
            user=request.user,
            ingredient=ingredient, 
            data=data, 
            thumb=thumb, 
            grams_in_hint=form.data['grams_in_hint'])
        hint.save()   
        return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))
    context = {"form":form,"pk":pk}
    template = "hint_add.html"
    return render(request, template, context)

@login_required
def ingredient_hint_delete(request, pk, hint_id):
    hint = models.IngredientHint.objects.get(id=hint_id)
    hint.delete()
    return HttpResponseRedirect(reverse('ingredients:details'))    

@login_required
def ingredient_hint_details(request, pk, hint_id):
    hint = models.IngredientHint.objects.get(id=hint_id)
    form = forms.IngredientHintForm(request.POST or None, instance=hint)
    if form.is_valid():
        hint.grams_in_hint = form.data['grams_in_hint']
        hint.save()
        return HttpResponseRedirect(reverse('ingredients:details', kwargs={'pk':pk}))
    context = {"form":form,"pk":pk,"hint_id":hint_id, "data":hint.data}
    template = "hint_edit.html"
    return render(request, template, context)   