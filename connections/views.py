from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .models import Connection
from tokens.models import Tokens
from .protector import encrypt_and_truncate
from .helpers import sanitize_token, calculate_minutes_passed
# Create your views here.
@login_required
@csrf_protect
def connect(request):
    if request.method == 'GET':
        return render(request, 'connect.html')
    elif request.method == 'POST':
        token = sanitize_token(request.POST.get('token'))
        token_obj = Tokens.objects.get(token=token)
        
        if not token_obj or calculate_minutes_passed(token=token_obj) == True:
            if token_obj:
                token_obj.delete()
            messages.error(request, 'Invalid token')
            return redirect('index')
        
        user_one = User.objects.get(pk=request.user.id)
        user_two = token_obj.user
        try:
            connection = Connection(user_one=user_one, user_two=user_two)
            connection.save()
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('index')
        token_obj.delete()
        messages.success(request, f'Successfully connected with {user_two.username}')
        return redirect('options')
    else:
        messages.error(request, 'Invalid method')
        return redirect('index')
    
@login_required
def my_connections(request):
    user_obj = get_object_or_404(User, pk=request.user.id)
    connections = Connection.objects.get(user_one=user_obj)
    return render(request, 'my_connections.html', {'user': user_obj}) 

@login_required
def options(request):
    user = get_object_or_404(User, pk=request.user.id)
    connections = Connection.objects.filter(Q(user_one=user) | Q(user_two=user))
    connections_for_view = []
    for connection in connections:
        other_user = connection.user_one if connection.user_two == user else connection.user_two
        connections_for_view.append({'connection': other_user, 'encrypted_id': encrypt_and_truncate(connection.id)})
    return render(request, 'connections.html', {'users': connections_for_view})