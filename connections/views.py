from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Connection
from tokens.models import Tokens
from .helpers import sanitize_token, calculate_minutes_passed
# Create your views here.
@login_required
@csrf_protect
def connect(request):
    if request.method == 'GET':
        print('get')
        return render(request, 'connect.html')
    elif request.method == 'POST':
        token = sanitize_token(request.POST.get('token'))
        token_obj = Tokens.objects.get(token=token)
        print('here')
        if not token_obj or calculate_minutes_passed(token=token_obj) >= 15:
            if token_obj:
                token_obj.delete()
            messages.error(request, 'Invalid token')
            return redirect('index')
        
        return redirect('my_connections')
    else:
        print('else')
        messages.error(request, 'Invalid method')
        return redirect('index')
    
@login_required
def my_connections(request):
    user_obj = get_object_or_404(User, pk=request.user.id)
    return render(request, 'my_connections.html', {'user': user_obj}) 