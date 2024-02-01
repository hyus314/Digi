from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse

from html import escape

from .validations import validate_username, validate_names, validate_password, validate_email

@csrf_protect
def register(request):
    if request.method == "GET":
        if request.GET.get('username'):
            username = request.GET.get('username')
            user_exists = User.objects.filter(username=username).exists()
            return JsonResponse({'exists': user_exists})
        return render(request, 'register.html')
    
    username = escape(request.POST.get('username'))
    first_name = escape(request.POST.get('first'))
    last_name = escape(request.POST.get('last'))
    email = escape(request.POST.get('email'))
    password = escape(request.POST.get('password'))
    confirmation = escape(request.POST.get('confirmation'))

    if validate_username(username) == False:
        return render(request, 'register.html', {'message': 'Username is not valid'})
    if validate_names(first_name, last_name) == False:
        return render(request, 'register.html', {'message': 'Name is not valid'})
    if validate_password(password, confirmation) == False:
        return render(request, 'register.html', {'message': 'Password is not valid'})
    if validate_email(email) == False:
        return render(request, 'register.html', {'message': 'Email is not valid'})

    new_user = User.objects.create_user(username, email, password)

    new_user.first_name = first_name
    new_user.last_name = last_name

    new_user.save()

    messages.success(request, 'Registered successfully!')
    return redirect('index')


@csrf_protect
@login_required
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    username = escape(request.POST.get('username'))
    password = escape(request.POST.get('password'))

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        return redirect('index')  
    else:
        return render(request, 'login.html', {'message': 'Invalid username or password'})
    

def logout_view(request):
    logout(request)
    return redirect('index')

def account_exists(request):
    if request.method == "GET":
        username = request.GET.get('username')
        user_exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': user_exists})