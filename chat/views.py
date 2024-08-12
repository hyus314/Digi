from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Connection
from connections.protector import decrypt_data
import base64

def chat(request):
    chat_id = request.GET.get('id')
    return render(request, 'chat.html', {'chat_id': chat_id})

@login_required
def get_connection_user(request):
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
            
            # Get the currently logged-in user
            current_user = request.user
            
            # Determine the other user in the connection
            if connection.user_one == current_user:
                other_user = connection.user_two
            elif connection.user_two == current_user:
                other_user = connection.user_one
            else:
                return HttpResponseBadRequest('The current user is not part of this connection.')

            # Prepare the response data
            data = {
                'other_user': other_user.username,
            }
            
            # Return as a JSON response
            return JsonResponse(data)
        
        except Connection.DoesNotExist:
            return HttpResponseBadRequest('Invalid connection ID.')
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    
    return HttpResponseBadRequest('Invalid request method.')