from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse

from html import escape

from .validations import validate_username, validate_names, validate_password, validate_email
from .models import Tokens


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

    if User.objects.filter(username=username).exists():
        return render(request, 'register.html', {'message': 'User with that username already exists.'})
    if validate_username(username) == False:
        return render(request, 'register.html', {'message': 'Username is not valid.'})
    if validate_names(first_name, last_name) == False:
        return render(request, 'register.html', {'message': 'Name is not valid.'})
    if validate_password(password, confirmation) == False:
        return render(request, 'register.html', {'message': 'Password is not valid.'})
    if validate_email(email) == False:
        return render(request, 'register.html', {'message': 'Email is not valid.'})

    new_user = User.objects.create_user(username, email, password)

    new_user.first_name = first_name
    new_user.last_name = last_name

    new_user.save()

    messages.success(request, 'Registered successfully!')
    return redirect('index')


@csrf_protect
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
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def account_exists(request):
    if request.method == "GET":
        username = request.GET.get('username')
        user_exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': user_exists})
    
@login_required
def profile(request):
    user_id = request.user.id
    if not user_id:
        messages.error(request, 'User id not found.')
        return redirect('index')
    
    user_obj = get_object_or_404(User, pk=user_id)
    return render(request, 'profile.html', {'user': user_obj}) 

@login_required
def get_token(request):
    user_id = request.user.id
    if not user_id:
        messages.error(request, 'User id not found.')
        return redirect('index')
    
    if Tokens.token_exists_for_user(user_id):
        token_value = Tokens.get_token_value_for_user(user_id)
    else:
        user = User.objects.get(pk=user_id)
        token = Tokens(user)
        token_value = token.token
        token.save()
    
    return JsonResponse({'token': token_value})

@login_required
def token_exists(request):
    if request.method == "GET":
        user_id = request.user.id
        if not user_id:
            messages.error(request, 'User id not found.')
            return redirect('index')
        
        return JsonResponse({'result': Tokens.token_exists_for_user(user_id)})
    return JsonResponse({'result': False})

