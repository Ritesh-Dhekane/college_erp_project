from django.shortcuts import render
from datetime import datetime

def home(request):
    return render(request, 'home.html', {'year': datetime.now().year})

def register(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def library(request):
    return render(request, 'library.html')
