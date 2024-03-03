from django.shortcuts import  redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse

from .models import Tokens
from .validations import validate_input

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
        validation_errors = validate_input(data)
        if validation_errors:
            for error in validation_errors:
                messages.error(request, error)
            return redirect('index')
        print(data)
        day = int(data.get('day'))
        hours = int(data.get('hours'))
        minutes = int(data.get('minutes'))
        seconds = int(data.get('seconds'))
        offset = int(data.get('offset'))
        user = User.objects.get(pk=user_id)
        token = Tokens(user=user)
        token.save(day=day, hours=hours, minutes=minutes, seconds=seconds, offset=offset)
    
    return JsonResponse({'token_value': token.token, 'created_at': token.created_at.strftime('%Y-%m-%d %H:%M:%S')})

@login_required
def token_exists(request):
    if request.method == "GET":
        user_id = request.user.id
        if not user_id:
            messages.error(request, 'User id not found.')
            return redirect('index')
        
        return JsonResponse({'result': Tokens.token_exists_for_user(user_id)})
    return JsonResponse({'result': False})

@login_required
def set_timezone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        timezone_offset = data.get('timezone_offset')
        return JsonResponse({'message': 'Timezone set successfully'})
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

def check_token(request):
    if request.method == "POST":
        token_data = json.loads(request.body)
        token_value = token_data.get('token')
        try:
            token_object = Tokens.objects.get(token=token_value)
            
            # Token exists
            return JsonResponse({'message': 'yes'})
        except Tokens.DoesNotExist:
            # Token does not exist
            return JsonResponse({'message': 'no'})
    else:
        return JsonResponse({'message': 'does not exist'}, status=404)