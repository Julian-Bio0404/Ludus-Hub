"""Chat consummers."""

import json

# Channels
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# Permissions
from apps.chat.permissions import IsWebSocketAuthenticated

# Utils
from apps.utils.chat import create_message, get_messages


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """Chat consumer."""

    permission_classes = [IsWebSocketAuthenticated]

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
            self.room_group_name = self.scope['url_route']['kwargs']['room_name']
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
            await self.accept()
            messages = await get_messages(self.room_group_name)
            for text in messages:
                await self.channel_layer.group_send(
                    self.room_group_name, {'type': 'get_messages', 'message': text}
                )
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Leave room group."""
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        except AttributeError:
            return StopConsumer()

    async def receive_json(self, content, **kwargs):
        """
        Receive message from WebSocket
        and send message to room group.
        """
        message = content['message']
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'send_message', 'message': message}
        )

    async def send_message(self, content):
        """
        Receive message from room group
        and send message to WebSocket.
        """
        message = content['message']
        if message:
            user = self.scope['user']
            await create_message(
                username=user.username, room_name=self.room_group_name, text=message)
            await self.send(text_data=json.dumps({'message': message}))

    async def get_messages(self, content):
        """Get old messages."""
        message = content['message']
        await self.send(text_data=json.dumps({'message': message}))
