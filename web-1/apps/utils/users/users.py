"""Users utils."""

from datetime import timedelta

# Django
from django.conf import settings
from django.utils import timezone

# Django REST Framework
from rest_framework.authtoken.models import Token


def token_is_expired(token: Token) -> bool:
    """Check if a token is expired."""
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(days=settings.TOKEN_EXPIRE_IN) - time_elapsed
    return left_time < timedelta(seconds=0)
