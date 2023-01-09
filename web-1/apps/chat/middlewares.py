"""Chat middlewares."""

from urllib.parse import parse_qs

# Channels
from channels.db import database_sync_to_async

from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(scope):
    from rest_framework.authtoken.models import Token
    try:
        key = parse_qs(scope['query_string'].decode('utf8'))['token'][0]
        token = Token.objects.get(key=key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()
    except KeyError:
        return AnonymousUser()
    except ValueError:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that
    takes user IDs from the query string.
    """

    def __init__(self, app):
        """Store the ASGI application we were passed."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Look up user from query string."""
        scope['user'] = await get_user(scope)
        return await self.app(scope, receive, send)
