"""Chat consummers."""

import json

# Channels
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

# Permissions
from apps.chat.permissions import IsWebsocketAuthenticated


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat consumer."""

    permission_classes = [IsWebsocketAuthenticated]

    def get_permissions(self):
        return [p() for p in self.permission_classes]

    def check_permissions(self):
        permisions = self.get_permissions()
        for permission in permisions:
            if not permission.has_permission(self.scope):
                return False
        return True

    async def connect(self):
        """Join room group."""
        if self.check_permissions():
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        """Leave room group."""
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        except AttributeError:
            return StopConsumer()

    async def receive(self, text_data):
        """
        Receive message from WebSocket
        and send message to room group.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )

    async def chat_message(self, event):
        """
        Receive message from room group
        and send message to WebSocket.
        """
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
