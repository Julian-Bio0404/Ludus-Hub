"""Room models."""

# Django
from django.db import models

# Utils
from apps.utils.models import SportfyModel


class Message(SportfyModel):
    """Message model."""

    sender = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True)

    room = models.ForeignKey(
        'chat.Room', on_delete=models.CASCADE, related_name='messages')

    text = models.TextField(blank=True, max_length=1500)
