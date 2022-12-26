"""Chat utils."""

import typing as t

# Channels
from channels.db import database_sync_to_async

# Models
from apps.chat.models import Message, Room
from apps.users.models import User


@database_sync_to_async
def get_messages(room_name: str) -> t.Union[list[str], None]:
    """Return room messages if exixts by websockets."""
    room = Room.objects.filter(slug=room_name).last()
    if room:
        messages = room.messages.all().order_by('created')
        return [message.text for message in messages]


@database_sync_to_async
def create_message(username: str, room_name: str, text: str) -> None:
    """Create a message in db from websocket."""
    user = User.objects.filter(username=username).last()
    room = Room.objects.filter(slug=room_name).last()
    if room and user:
        Message.objects.create(sender=user, room=room, text=text)
