"""Chat views."""

# Django
from django.shortcuts import get_object_or_404, render

# Models
from apps.chat.models import Room


def room(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    return render(request, 'chat/room.html', {'room_name': room.slug})
