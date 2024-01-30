from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
# Create your views here.

@csrf_protect
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        return redirect('index')