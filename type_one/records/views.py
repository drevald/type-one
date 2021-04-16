from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.forms import ChoiceField
from datetime import datetime
from ..core.models import User, GlucoseUnit, Insulin
from ..ingredients.models import Ingredient, IngredientUnit
from .models import Record, Meal
from .forms import MealForm, RecordForm, LongForm, UploadFileForm, Photo
from PIL import Image, ImageFilter
from django.views.generic.edit import DeleteView
from . import models
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

import io
import base64

@login_required
def records(request):
    records_list = Record.objects.filter(user=request.user).order_by('-time')
    page = request.GET.get('page', 1)
    paginator = Paginator(records_list, 5)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)    
    template = loader.get_template('records.html')
    context = {'records' : records}
    return HttpResponse(template.render(context, request))

@login_required
def delete(request, pk):
    record = Record.objects.get(id = pk,user=request.user)
    record.delete()
    return HttpResponseRedirect(reverse('records:list'))

@method_decorator(login_required, name='delete')
class RecordDeleteView(DeleteView):
    model = models.Record
    template_name = 'record_delete.html'
    success_url = reverse_lazy('records:list')    

@login_required
def photo(request, pk):
    record = Record.objects.get(id = pk,user=request.user) 
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = handle_uploaded_file(request.FILES['file'])
            photo = Photo(record=record, data=data)
            photo.save()
            print("valid")
            return HttpResponseRedirect(reverse("records:details", kwargs={'pk':pk}))
    else:
        form = UploadFileForm()
        return render(request, 'photo.html', {'form': form,'pk':pk})

def handle_uploaded_file(f):
    im = Image.open(f)        
    size = (360, 240)
    im.thumbnail(size)
    memstr = io.BytesIO()
    im.save(memstr, 'JPEG')
    memstr.seek(0)
    data = base64.b64encode(memstr.read()).decode('utf-8') 
    return data    

@login_required
def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record.objects.get(id=pk,user=request.user)    
    return store(request, record)

@login_required
def create(request, type=0):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record(glucose_level_unit = request.user.glucose_level_unit, type=type,user=request.user)
    record.insulin = request.user.rapid_acting_insulin if type==0 else request.user.long_acting_insulin
    return store(request, record)

@login_required
def store(request, record):
    print(record.glucose_level)
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    meals = Meal.objects.filter(record=record.id) if record.id else None
    photos = Photo.objects.filter(record=record.id) if record.id else None
    meal_details = [str(meal) for meal in meals] if meals else None
    meal_details_str = ','.join(meal_details) if meal_details else None
    breads = [meal.quantity * meal.ingredient_unit.grams_in_unit * meal.ingredient_unit.ingredient.bread_units_per_100g for meal in meals] if meals else None
    record.bread_units = sum(breads)/100 if meals else record.bread_units 
    record.bread_units = round(record.bread_units, 1)
    form = RecordForm(request.POST or None, instance=record) if record.type == 0 else LongForm(request.POST or None, instance=record)        
    print(form)
    if form.is_valid():
        form.instance.bread_units = round(form.cleaned_data['bread_units'], 1) if record.type == 0 else 0
        form.save()
        print("Returning to " + reverse('records:list'))
        return HttpResponseRedirect(reverse('records:list'))
    context = {"form":form, "meals":meals, "photos":photos, "meal_details":meal_details_str}
    return render(request, template, context)

@login_required
def meals(request, pk):
    meals = Meal.objects.filter(record=Record.objects.get(id=pk),user=request.user)
    template = 'meals.html'
    context = {'meals' : meals, 'pk' : pk}
    return render(request, template, context)

@login_required
def meals_create(request, pk):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))        
    # meal = Meal(record=Record.objects.get(id=pk), ingredient_unit=IngredientUnit.objects.first(),user=request.user)
    form = MealForm(request.POST or None)
    if form.is_valid():
        quantity = form.data["quantity"]
        ingredient_unit_id = form.data["ingredient_unit"]
        ingredient_unit = IngredientUnit.objects.get(id=ingredient_unit_id)
        record = Record.objects.get(id=pk)
        meal = Meal(ingredient_unit=ingredient_unit, quantity=quantity, record=record, user=request.user)
        meal.save()        
        return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))
    template = 'meal_new.html'
    context = {'form':form}
    return render(request, template, context)

@login_required
def meals_details(request, pk, meal_id):   
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))        
    meal = Meal.objects.get(id=meal_id,user=request.user)    
    form = MealForm(request.POST or None, instance=meal)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))
    template = 'meal_new.html'
    return render(request, template, {'form':form})

@login_required
def meals_delete(request, pk, meal_id):  
    meal = Meal.objects.get(id = meal_id,user=request.user)
    meal.delete()
    return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))

@login_required
def recent(request, pk):    
    list = Record.objects.exclude(id=pk,user=request.user)
    template = "meals_recent.html"
    context = {'pk':pk,'list':list}
    return render(request, template, context) 

@login_required
def select(request, pk, record_id):   
    print(record_id)
    meals = Record.objects.get(id=record_id,user=request.user).meals.filter(user=request.user)
    record = Record.objects.get(id=pk)
    for meal in meals:
        imported_meal = Meal(
            ingredient_unit=meal.ingredient_unit, 
            quantity=meal.quantity,
            record=record,
            user=request.user)
        imported_meal.save()
        print(imported_meal)
    return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))

@login_required
def photo_edit(request, pk, photo_id):
    template = "photo_edit.html"
    photo = Photo.objects.filter(id=photo_id).first()
    context = {'pk':pk,'photo':photo}
    return render(request, template, context)

@login_required
def photo_delete(request, pk, photo_id):
    photo = Photo.objects.filter(id=photo_id).first()
    photo.delete()
    return HttpResponseRedirect(reverse("records:details", kwargs={'pk':pk}))
