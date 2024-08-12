import json, base64

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from connections.protector import decrypt_data

from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        encoded_room_name = self.scope['url_route']['kwargs']['room_name']
        encrypted_room_name_bytes = base64.urlsafe_b64decode(encoded_room_name)
        self.room_name = decrypt_data(encrypted_room_name_bytes)
        
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(text_data)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Check if the user is authenticated
        if self.scope['user'].is_authenticated:
            username = self.scope['user'].username  # The user who sent the message
            # Include the username in the message
            self.send(text_data=json.dumps({
                "message": message,
                "username": username  # This is the sender's username
            }))
        else:
            # Handle the case where the user is not authenticated
            self.send(text_data=json.dumps({
                "message": "User not authenticated"
            }))