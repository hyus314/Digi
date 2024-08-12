from django.shortcuts import render

import json
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Connection
from connections.protector import decrypt_data
import base64

def chat(request):
    chat_id = request.GET.get('id')
    return render(request, 'chat.html', {'chat_id': chat_id})

def get_connection_users(request):
    if request.method == 'GET':
        encrypted_connection_id = request.GET.get('connection_id')
        
        if not encrypted_connection_id:
            return HttpResponseBadRequest('No connection ID provided.')

        try:
            # Decode the base64 encoded connection ID
            encrypted_connection_id_bytes = base64.urlsafe_b64decode(encrypted_connection_id)
            
            # Decrypt the connection ID
            connection_id = decrypt_data(encrypted_connection_id_bytes)
            
            # Convert to an integer (since IDs are usually integers)
            connection_id = int(connection_id)
            
            # Retrieve the connection from the database
            connection = Connection.objects.get(pk=connection_id)
            
            # Prepare the response data
            data = {
                'user_one': connection.user_one.username,
                'user_two': connection.user_two.username,
            }
            
            # Return as a JSON response
            return JsonResponse(data)
        
        except Connection.DoesNotExist:
            return HttpResponseBadRequest('Invalid connection ID.')
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    
    return HttpResponseBadRequest('Invalid request method.')