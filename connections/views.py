from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

# Create your views here.
@login_required
@csrf_protect
def connect(request):
    if request.method == 'GET':
        return render(request, 'connect.html')
    elif request.method == 'POST':
        return redirect('connections')
    else:
        return redirect('index')
    
@login_required
def my_connections(request):
    user_obj = get_object_or_404(User, pk=request.user.id)
    return render(request, 'my_connections.html', {'user': user_obj}) 