import json, base64

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from connections.protector import decrypt_data, encrypt_msg, decrypt_msg
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
            encrypted_message_id = encrypt_msg(msg.id)  # Encrypt the message ID
            self.chat_message({
                "message": msg.message,
                "user": msg.sender.username,
                "message_id": encrypted_message_id,  # Include the encrypted message ID
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
        encrypted_message_id = text_data_json.get("message_id")
        
        if encrypted_message_id:
            try:
                message_id = decrypt_data(encrypted_message_id)
            except Exception as e:
                print(f"Failed to decrypt message ID: {e}")
                return

        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            print(f"Message with ID {message_id} does not exist.")
            return

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
        encrypted_message_id = encrypt_msg(message.id)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_content,
                "user": sender_username,
                "message_id": encrypted_message_id,  # Send the encrypted message ID
            }
        )
        
    # Send message to room group
    def chat_message(self, event):
        message = event["message"]
        user = event["user"]  # Get the sender's username

    # Send message back to WebSocket with the sender's username and encrypted message ID
        self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            "message_id": event.get("message_id"),  # Pass the message ID if available
        }))