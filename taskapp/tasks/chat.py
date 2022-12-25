"""Users tasks."""

from __future__ import absolute_import, unicode_literals

# Celery
from taskapp.celery import app

# Models
from apps.chat.models import Message, Room


@app.task(bind=True)
def create_message(self, sender, room_name, text):
    """Create a message in db from websocket."""
    room = Room.objects.filter(slug=room_name).last()
    if room:
        Message.objects.create(sender=sender, room=room, text=text)
