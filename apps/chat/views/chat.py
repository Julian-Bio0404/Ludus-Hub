"""Chat views."""

# Django
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Django REST Framework
from rest_framework.authtoken.models import Token

# Models
from apps.chat.models import Room

# Utils
from apps.utils.users import token_is_expired


def room(request, room_name):
    """Chat room function view."""
    try:
        key = request.get_full_path().split('?token=')[1]
        token = Token.objects.get(key=key)
        if token_is_expired(token):
            raise Http404('You must login again.')
        user = token.user
        room = get_object_or_404(Room, slug=room_name)
        if user not in room.receivers.all():
            raise Http404('Room does not exist.')
        return render(request, 'chat/room.html', {'room_name': room.slug})
    except IndexError:
        raise Http404('Page not found.')
    except Token.DoesNotExist:
        raise Http404('Token does not exist.')
