import json, base64

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from connections.protector import decrypt_data
from .models import Message
from connections.models import Connection
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

        # Retrieve all messages related to this chat room from the database
        connection = Connection.objects.get(pk=self.room_name)
        messages = Message.objects.filter(connection=connection)

        # Send each message to the client directly (not via group_send)
        for msg in messages:
            self.chat_message({
                "message": msg.message,
                "user": msg.sender.username,
            })


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
        message_content = text_data_json.get("message")
        sender_username = text_data_json.get("user")
        
        # Print the received data to the server console
        print(f"Received message: '{message_content}' from user: {sender_username}")
        
        # Retrieve the user object for the sender
        try:
            sender = User.objects.get(username=sender_username)
        except User.DoesNotExist:
            print(f"User {sender_username} does not exist.")
            return

        # Retrieve the connection object based on the room name
        try:
            connection = Connection.objects.get(id=self.room_name)
        except Connection.DoesNotExist:
            print(f"Connection with ID {self.room_name} does not exist.")
            return

        # Save the message to the database
        message = Message.objects.create(
            connection=connection,
            message=message_content,
            sender=sender
        )

        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_content,
                "user": sender_username,  # Pass the sender's username
            }
        )
    # Send message to room group
    def chat_message(self, event):
        message = event["message"]
        user = event["user"]  # Get the sender's username

        # Send message back to WebSocket with the sender's username
        self.send(text_data=json.dumps({
            "message": message,
            "user": user,
        }))
