from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import forms

def signin(request):
    form = forms.LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            url = request.GET.get('next') if request.GET.get('next') else "/"
            return HttpResponseRedirect(url)
        else:
            return HttpResponse("Fails")
    return render(request, "login.html", {"form":form})

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:signin'))
