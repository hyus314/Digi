from django.shortcuts import  redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse

from .models import Tokens

import json
import datetime

@login_required
@csrf_protect
def get_token(request):
    user_id = request.user.id
    if not user_id:
        messages.error(request, 'User id not found.')
        return redirect('index')
    
    if Tokens.token_exists_for_user(user_id):
        token = Tokens.get_token_value_for_user(user_id)
    else:
        data = json.loads(request.body)
        day = int(data.get('day'))
        hours = int(data.get('hours'))
        minutes = int(data.get('minutes'))
        user = User.objects.get(pk=user_id)
        token = Tokens(user=user)
        token.save(day=day, hours=hours, minutes=minutes)
    
    token_value = {'token_value': token.token, 'created_at': token.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    return JsonResponse({'token': json.dumps(token_value)})

@login_required
def token_exists(request):
    if request.method == "GET":
        user_id = request.user.id
        if not user_id:
            messages.error(request, 'User id not found.')
            return redirect('index')
        
        return JsonResponse({'result': Tokens.token_exists_for_user(user_id)})
    return JsonResponse({'result': False})

