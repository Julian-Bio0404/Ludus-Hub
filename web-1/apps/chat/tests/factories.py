# Channels
from channels.db import database_sync_to_async

# Django REST Framework
from rest_framework.authtoken.models import Token

# Factories
from apps.sports.tests.factories import ClubFactory
from apps.users.tests.factories import UserFactory


@database_sync_to_async
def get_club_factory(**kwargs):
    return ClubFactory(**kwargs)


@database_sync_to_async
def get_room(club):
    return club.room


@database_sync_to_async
def get_user_factory():
    return UserFactory()


@database_sync_to_async
def get_token(user):
    token = Token.objects.create(user=user)
    return token.key
