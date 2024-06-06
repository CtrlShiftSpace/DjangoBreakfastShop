from django.shortcuts import render

from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'dashboard/index.html', {})
