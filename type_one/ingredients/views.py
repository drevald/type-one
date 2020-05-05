from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def ingredients(request):
    records_list = Ingredient.objects.all()
    return HttpResponse("ingredients")