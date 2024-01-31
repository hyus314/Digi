from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
# Create your views here.

@csrf_protect
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    
    username = request.POST.get('username')
    first_name = request.POST.get('first')
    last_name = request.POST.get('last')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirmation = request.POST.get('confirmation')

    print(username)
    print(first_name)
    print(last_name)
    print(email)
    print(password)
    print(confirmation)
    return redirect('index')