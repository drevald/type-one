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
from django.db.models import Min, Max
from django.utils.timezone import make_aware

import pytz

import calendar
import io
import base64

# SELECT 
#     it.name AS ingredient_type,
#     SUM(rm.quantity * iu.grams_in_unit) AS total_grams
# FROM records_meal rm
# JOIN ingredients_ingredientunit iu ON rm.ingredient_unit_id = iu.id
# JOIN ingredients_ingredient i ON iu.ingredient_id = i.id
# JOIN ingredients_ingredienttype iit ON i.id = iit.ingredient_id
# JOIN ingredients_type it ON iit.type_id = it.id
# JOIN records_record rr ON rm.record_id = rr.id
# WHERE rr.time::DATE = '2025-02-21'  -- Replace with the desired date
# GROUP BY it.name
# ORDER BY total_grams DESC;

# SELECT 
#     SUM(rm.quantity * iu.grams_in_unit * i.fat_per_100g / 100) AS total_fat,
#     SUM(rm.quantity * iu.grams_in_unit * i.protein_per_100g / 100) AS total_protein,
#     SUM(rm.quantity * iu.grams_in_unit * i.carbohydrate_per_100g / 100) AS total_carbohydrates
# FROM records_meal rm
# JOIN ingredients_ingredientunit iu ON rm.ingredient_unit_id = iu.id
# JOIN ingredients_ingredient i ON iu.ingredient_id = i.id
# JOIN ingredients_ingredienttype iit ON i.id = iit.ingredient_id
# JOIN ingredients_type it ON iit.type_id = it.id
# JOIN records_record rr ON rm.record_id = rr.id
# WHERE rr.time::DATE = '2025-02-19'  -- Replace with the desired date
# ORDER BY total_carbohydrates DESC;

@login_required
def records(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    if year and month and day:
        today = make_aware(datetime(int(year), int(month), int(day)))
    else:
        today = make_aware(datetime.now())

    # Define strict boundaries for filtering
    start_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999)

    records = Record.objects.filter(
        time__gte=start_time, 
        time__lte=end_time, 
        user=request.user
    ).order_by('time')

    # Get the previous day correctly
    # prev_day = Record.objects.filter(time__lt=start_time).aggregate(prev_day=Max('time')).get('prev_day')
    prev_day = (Record.objects.filter(time__lt=start_time).aggregate(prev_day=Max("time")).get("prev_day"))
    # FIX: Use `end_time` to exclude today and get the real next day
    next_day = Record.objects.filter(time__gt=end_time).aggregate(next_day=Min('time')).get('next_day')

    print(f"Prev Day: {prev_day}")
    print(f"Next Day: {next_day}")

    template = loader.get_template('records.html')
    context = {'records' : records, 'next_day':next_day, 'prev_day':prev_day}
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
    from django.db.models import Count
    all_records = (Record.objects
        .filter(user=request.user)
        .exclude(id=pk)
        .annotate(meal_count=Count('meals'))
        .filter(meal_count__gt=0)
        .order_by('-time')
        .prefetch_related('meals'))
    paginator = Paginator(all_records, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    template = "meals_recent.html"
    context = {'pk': pk, 'list': page_obj}
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
def report(request):
    import csv
    if 'start' in request.GET or 'preset' in request.GET:
        preset = request.GET.get('preset')
        if preset == '7days':
            end = datetime.now()
            start = end - timedelta(days=7)
        elif preset == '30days':
            end = datetime.now()
            start = end - timedelta(days=30)
        else:
            try:
                start = datetime.strptime(request.GET.get('start', ''), '%Y-%m-%d')
                end = datetime.strptime(request.GET.get('end', ''), '%Y-%m-%d')
            except ValueError:
                return render(request, 'report.html', {'error': 'Invalid date format'})

        start = make_aware(start.replace(hour=0, minute=0, second=0, microsecond=0))
        end = make_aware(end.replace(hour=23, minute=59, second=59, microsecond=999999))

        from django.db.models import Prefetch
        records = Record.objects.filter(
            user=request.user, time__gte=start, time__lte=end
        ).order_by('time').select_related('insulin').prefetch_related(
            Prefetch('meals', queryset=Meal.objects.select_related(
                'ingredient_unit__ingredient',
                'ingredient_unit__unit'
            ))
        )

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="report_{start.strftime("%Y%m%d")}_{end.strftime("%Y%m%d")}.csv"'
        response.write('\ufeff')  # UTF-8 BOM for Excel

        writer = csv.writer(response)

        header = ['Time']
        if request.user.show_rapid_insulin or request.user.show_long_insulin:
            header += ['Insulin amount', 'Insulin']
        if request.user.show_sugar:
            header.append('Glucose level')
        if request.user.show_bread_units:
            header.append('Bread units')
        if request.user.show_calories:
            header.append('Calories')
        header += ['Notes', 'Ingredient', 'Unit', 'Quantity', 'Carbs (g)', 'Fat (g)', 'Protein (g)', 'Cal (kcal)']
        writer.writerow(header)

        for record in records:
            meals = record.meals.all()
            record_row = [record.time.strftime('%Y-%m-%d %H:%M')]
            if request.user.show_rapid_insulin or request.user.show_long_insulin:
                record_row.append(record.insulin_amount or '')
                record_row.append(record.insulin.name if record.insulin else '')
            if request.user.show_sugar:
                record_row.append(record.glucose_level or '')
            if request.user.show_bread_units:
                record_row.append(record.bread_units or '')
            if request.user.show_calories:
                record_row.append(record.calories or '')
            record_row.append(record.notes or '')

            if meals:
                for m in meals:
                    ing = m.ingredient_unit.ingredient
                    grams = m.quantity * m.ingredient_unit.grams_in_unit
                    writer.writerow(record_row + [
                        ing.name,
                        m.ingredient_unit.unit.name,
                        m.quantity,
                        round(grams * ing.carbohydrate_per_100g / 100, 1),
                        round(grams * ing.fat_per_100g / 100, 1),
                        round(grams * ing.protein_per_100g / 100, 1),
                        round(grams * ing.energy_kKkal_per_100g / 100, 1),
                    ])
            else:
                writer.writerow(record_row + ['', '', '', '', '', '', ''])

        return response

    return render(request, 'report.html')

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
