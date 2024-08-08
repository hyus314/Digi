import json, base64

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from connections.protector import decrypt_data

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        encrypted_room_name = self.scope["url_route"]["kwargs"]["room_name"]
        encrypted_room_name_bytes = encrypted_room_name
        print(encrypted_room_name_bytes + 'this is the text')
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

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))