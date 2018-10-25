from django.shortcuts import render
from .reisplanner import *

def home(request):
    return render(request, 'home.html', {})

def reisplanner(request):
    form = createForm(request)
    result = main()

    return render(request, 'reisplanner.html', {'form': form, 'vertrekTijd': result['vertrekTijd'], 'actueleReisTijd': result['actueleReisTijd'], 'status': result['status'], 'aantalOverstappen': result['aantalOverstappen']})