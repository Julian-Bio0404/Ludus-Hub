"""Chat URLs."""

# Django
from django.urls import path

# Views
from apps.chat.views import room

app_name = 'chat'

urlpatterns = [path('<str:room_name>/', room, name='room')]
