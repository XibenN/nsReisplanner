from django.shortcuts import render
from .reisplanner import *

def home(request):
    return render(request, 'home.html', {})

def reisplanner(request):
    form = createForm(request)
    return render(request, 'reisplanner.html', {'form': form, 'apiData': main})