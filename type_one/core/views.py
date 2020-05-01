from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import Record, Insulin
from datetime import datetime

def records_list(request):
    records_list = Record.objects.all()
    print(records_list)
    template = loader.get_template('records_list.html')
    context = {'records_list' : records_list}
    return HttpResponse(template.render(context, request))

def record_new(request):
    record = Record()
    template = loader.get_template('record_new.html')
    context = {'record' : Record(), 'insulins':Insulin.objects.all()}
    return HttpResponse(template.render(context, request))

def record_create(request):
    record = Record()
    record.time = datetime.now()
    record.glucose_level =  request.POST['glucose_level']
    record.glucose_level_unit = request.user.glucose_level_unit
    record.insulin_amount = request.POST['insulin_amount']
    record.insulin = request.user.rapid_acting_insulin
    record.notes = request.POST.get('notes')
    record.save()    
    return HttpResponseRedirect(reverse('list'))

def record_delete(request, pk):
    record = Record.objects.get(id = pk)
    record.delete()
    return HttpResponseRedirect(reverse('list'))

def record_update(request, pk):
    record = Record.objects.get(id = pk)
    template = loader.get_template('record_new.html')
    context = {'record' : Record(), 'insulins':Insulin.objects.all()}
    return HttpResponse(template.render(context, request))