from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from html import escape

from .validations import validate_username, validate_names, validate_password, validate_email

@csrf_protect
def register(request):
    if request.method == "GET":
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
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    username = escape(request.POST.get('username'))
    password = escape(request.POST.get('password'))

    # Authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # User authentication successful, log the user in
        auth_login(request, user)
        return redirect('index')  # Redirect to the index page or any other desired page
    else:
        # Authentication failed, return login page with error message
        return render(request, 'login.html', {'message': 'Invalid username or password'})
    

def logout_view(request):
    logout(request)
    return redirect('index')