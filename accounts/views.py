from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        return render(request, 'index.html')