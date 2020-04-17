from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Insulin

class Home(TemplateView):
    template_name = 'index.html'

class Spisok(ListView):
    template_name = 'spisok.html'
    model = Insulin