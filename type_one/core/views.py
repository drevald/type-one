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
    template = loader.get_template('record_new.html')
    record = Record()
    context = {'record' : Record(), 'insulins':Insulin.objects.all()}
    return HttpResponse(template.render(context, request))

def record_create(request):
    record = Record()
    record.time = datetime.now()
    record.notes = request.POST.get('glucose_level')
    record.notes = request.POST.get('insulin_amount')
    record.notes = request.POST.get('notes')
    record.save()    
    return HttpResponseRedirect(reverse('list'))