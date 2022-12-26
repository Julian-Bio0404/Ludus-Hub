"""Chat views."""

# Django
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Django REST Framework
from rest_framework.authtoken.models import Token

# Models
from apps.chat.models import Room


def room(request, room_name):
    try:
        key = request.get_full_path().split('?token=')[1]
        token = Token.objects.get(key=key)
        user = token.user
        room = get_object_or_404(Room, slug=room_name)
        if user not in room.receivers.all():
            raise Http404('Room does not exist.')
        return render(request, 'chat/room.html', {'room_name': room.slug})
    except IndexError:
        raise Http404('Room does not exist.')
    except Token.DoesNotExist:
        raise Http404('Token does not exist.')
