from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.forms import ChoiceField
from datetime import datetime
from datetime import timedelta
from ..core.models import User, GlucoseUnit, Insulin
from ..ingredients.models import Ingredient, IngredientUnit, Type
from .models import Record, Meal 
from .forms import MealForm, RecordForm, LongForm, UploadFileForm, Photo
from PIL import Image, ImageDraw
from django.views.generic.edit import DeleteView
from . import models
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import TruncDate

import calendar
import io
import base64

@login_required
def records(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    # Check if year, month, and day are not None and are not empty strings
    if year and month and day:
        today = datetime(int(year), int(month), int(day))  # Convert to integers
    else:
        today = datetime.now() 
    # today_start = datetime(today.year, today.month, today.day, 00, 00, 00)

    # today_shifted = today_start + timedelta(hours = -3)
    # params = [today_shifted.year, today_shifted.month, today_shifted.day, today_shifted.hour, request.user.id]
    # records = Record.objects.raw('SELECT id, time FROM records_record where time > make_timestamp(%s, %s, %s, %s, 0, 0) and user_id=%s ORDER BY time DESC', params)
    
    
    # Calculate the start and end times for the given day
    start_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Fetch records for that specific day
    records = Record.objects.filter(
        time__gte=start_time, 
        time__lte=end_time, 
        user=request.user
    ).order_by('-time')
    
    
    template = loader.get_template('records.html')
    context = {'records' : records}
    return HttpResponse(template.render(context, request))

@login_required
def calendar_view(request, year=None, month=None):
    # Get year and month from query string or use current year and month
    year = request.GET.get('year', datetime.now().year)  # Default to current year if not provided
    month = request.GET.get('month', datetime.now().month)  # Default to current month if not provided

    # Convert to integers
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        year = datetime.now().year
        month = datetime.now().month

    # Validate month (must be between 1 and 12)
    if not (1 <= month <= 12):
        month = datetime.now().month  # Default to current month if invalid month is provided

    # Create "today" using the provided year and month
    today = datetime(year, month, 1)

    # Generate a matrix where each sub-list represents a week
    month_weeks = calendar.monthcalendar(year, month)

    # Validate month (must be between 1 and 12)
    if not (1 <= month <= 12):
        month = today.month  # Default to current month if invalid month is provided

    # Calculate previous and next month
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    
    # Adjust the year if month changes
    if month == 1:  # Previous month is December, so year must be adjusted
        prev_year = year - 1
    else:
        prev_year = year

    if month == 12:  # Next month is January, so year must be adjusted
        next_year = year + 1
    else:
        next_year = year

    calories_per_day = (
        Record.objects
        .filter(time__year=year, time__month=month)  # Filter by current month
        .values(day=TruncDate('time'))  # Group by date
        .annotate(total_calories=Sum('calories'))  # Sum calories
        .order_by('day')
    )

    # Convert to a dictionary with day as key
    calories_dict = {entry['day'].day: entry['total_calories'] for entry in calories_per_day}

    # Transform the data structure to include custom data
    structured_weeks = []
    for week in month_weeks:
        structured_week = []
        for day in week:
            if day == 0:
                structured_week.append(None)  # Empty day slot
            else:
                structured_week.append({
                    "day": day,
                    "event": calories_dict.get(day, None),
                  })
        structured_weeks.append(structured_week)

    month_name = datetime(year, month, 1).strftime("%B")  # Converts 3 → "March"
    
    return render(request, 'calendar.html', {
        "weeks": structured_weeks,
        "month_name": month_name,
        "month": month,
        "year": year,
        'prev_month': prev_month,
        'next_month': next_month,
        'prev_year': prev_year,
        'next_year': next_year,
        'month_name': month_name,
        'month_weeks': month_weeks,
    })

@login_required
def diagram(request):
    today = datetime.now()  
    today_start = datetime(today.year, today.month, today.day, 00, 00, 00)
    today_shifted = today_start + timedelta(hours = -3)
    t = [today_shifted.year, today_shifted.month, today_shifted.day, today_shifted.hour]
    records = Record.objects.raw('SELECT id, time FROM records_record where time > make_timestamp(%s, %s, %s, %s, 0, 0) ORDER BY time ASC', t)
    diagram_data = []
    if len(records) > 1:
        prot = records[1].get_prots()
        fat = records[1].get_fats()
        carb = records[1].get_carbs()
        for i in range(2, len(records)):
            diagram_data.append((
                records[i-1].time.hour + 3 + records[i-1].time.minute/60, 
                prot,
                fat,
                carb,
                records[i].time.hour + 3 + records[i].time.minute/60, 
                prot + records[i].get_prots(), 
                fat + records[i].get_fats(), 
                carb + records[i].get_carbs()
            ))
            prot += records[i].get_prots() 
            fat += records[i].get_fats() 
            carb += records[i].get_carbs()


    template = loader.get_template('diagram.html')
    context = {"data":diagram_data}
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
            (thumb, data) = handle_uploaded_file(request.FILES['file'])
            photo = Photo(record=record, data=data, thumb=thumb)
            photo.save()
            print("valid")
            return HttpResponseRedirect(reverse("records:details", kwargs={'pk':pk}))
    else:
        form = UploadFileForm()
        return render(request, 'photo.html', {'form': form,'pk':pk})

def handle_uploaded_file(f):
    im = Image.open(f)        
    size = (360, 240)
    im.thumbnail((360, 240))
    memstr = io.BytesIO()
    im.save(memstr, 'JPEG')
    memstr.seek(0)
    preview_data = base64.b64encode(memstr.read()).decode('utf-8') 
    im = Image.open(f)        
    im.thumbnail((100, 100))
    memstr = io.BytesIO()
    im.save(memstr, 'JPEG')
    memstr.seek(0)
    thumb_data = base64.b64encode(memstr.read()).decode('utf-8') 
    return thumb_data, preview_data    

@login_required
def details(request, pk):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record.objects.get(id=pk,user=request.user)    
    return store(request, record, record.type)

@login_required
def create(request, type=0):    
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:list'))    
    record = Record(glucose_level_unit = request.user.glucose_level_unit, type=type, user=request.user)
    record.insulin = request.user.rapid_acting_insulin if type==0 else request.user.long_acting_insulin
    record.save()
    return HttpResponseRedirect(reverse("records:details", kwargs={'pk':record.id}))

@login_required
def store(request, record, type):
    print(record.glucose_level)
    template = 'record_new.html' if record.type == 0 else 'record_long.html'
    meals = Meal.objects.filter(record=record.id) if record.id else None
    photos = Photo.objects.filter(record=record.id) if record.id else None
    meal_details = [str(meal) for meal in meals] if meals else None
    meal_details_str = ','.join(meal_details) if meal_details else None
    
    #recalculating calories if meal present
    calories = [meal.quantity * meal.ingredient_unit.grams_in_unit * meal.ingredient_unit.ingredient.energy_kKkal_per_100g for meal in meals] if meals else None
    record.calories = sum(calories)/100 if meals else record.calories
    record.calories = round(record.calories)

    #recalculating bread units if meal present
    breads = [meal.quantity * meal.ingredient_unit.grams_in_unit * meal.ingredient_unit.ingredient.bread_units_per_100g for meal in meals] if meals else None
    record.bread_units = sum(breads)/100 if meals else record.bread_units 
    record.bread_units = round(record.bread_units)    

    form = RecordForm(request.POST or None, instance=record) if record.type == 0 else LongForm(request.POST or None, instance=record)        
    if form.is_valid():
        form.instance.calories = 0 if form.cleaned_data['calories'] is None else (round(form.cleaned_data['calories'], 1) if record.type == 0 else 0)
        form.instance.bread_units = 0 if form.cleaned_data['bread_units'] is None else (round(form.cleaned_data['bread_units'], 1) if record.type == 0 else 0)
        form.instance.insulin = request.user.rapid_acting_insulin if type==0 else request.user.long_acting_insulin
        form.instance.glucose_level_unit = request.user.glucose_level_unit
        form.save()
        print("Returning to " + reverse('records:list'))
        return HttpResponseRedirect(reverse('records:list'))
    context = {"form":form, "meals":meals, "photos":photos, "meal_details":meal_details_str}
    return render(request, template, context)

@login_required
def meals(request, pk):
    meals = Meal.objects.filter(record=Record.objects.get(id=pk),user=request.user)
    types = Type.objects.all()
    template = 'meals.html'
    context = {'types':types, 'meals' : meals, 'pk' : pk}
    return render(request, template, context)

@login_required
def meals_create(request, pk, type_id):    
    print(type_id)
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('records:meals', kwargs={'pk':pk}))        
    form = MealForm(request.POST or None, initial={'type_id':type_id})
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
    # if "cancel" in request.POST:
    #     return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))        
    # meal = Meal.objects.get(id=meal_id,user=request.user)    
    # form = MealForm(request.POST or None, instance=meal)
    # if form.is_valid():
    #     form.save()
    #     return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))
    # template = 'meal_new.html'
    # return render(request, template, {'form':form})
    meal = models.Meal.objects.get(id=meal_id)
    if request.method == 'POST':
        form = MealForm(request.POST or None)
        if form.is_valid():
            meal.number = form.data['number']
            meal.ingredient_unit = form.data['ingredient_unit']
            meal.save()
            return HttpResponseRedirect(reverse('ingredients:types'))
    else:
        form = MealForm(initial={'meal':meal})    
    return render(request, "meal_edit.html", {"form":form})  

@login_required
def meals_delete(request, pk, meal_id):  
    meal = Meal.objects.get(id = meal_id,user=request.user)
    meal.delete()
    return HttpResponseRedirect(reverse("records:meals", kwargs={'pk':pk}))

@login_required
def recent(request, pk):    
    all_records = Record.objects.exclude(id=pk,user=request.user).prefetch_related('meals');
    #all_records = Record.objects.exclude(id=pk,user=request.user)
    records = []
    for record in all_records:
        if (len(record.meals.all())>0):
            records.append(record)
    print("records")
    template = "meals_recent.html"     
    context = {'pk':pk,'list':records}
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
