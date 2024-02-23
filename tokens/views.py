from django.shortcuts import  redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Tokens

# Create your views here.
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

