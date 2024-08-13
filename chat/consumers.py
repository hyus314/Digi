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
        # Load the JSON data sent from the frontend
        text_data_json = json.loads(text_data)
        
        # Extract the message and user from the data
        message = text_data_json.get("message")
        user = text_data_json.get("user")
        
        # Print the received data to the server console
        print(f"Received message: '{message}' from user: {user}")
        
        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "user": user,  # Pass the sender's username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        user = event["user"]  # Get the sender's username

        # Send message back to WebSocket with the sender's username
        self.send(text_data=json.dumps({
            "message": message,
            "user": user,
        }))
