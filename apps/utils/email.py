"""Email utils."""

# Utilities
from datetime import timedelta
import jwt

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


def token_generation(username: str, type: str, email=None) -> str:
    """Create JWT token."""
    exp_date = timezone.now() + timedelta(days=2)
    payload = {
        'user': username,
        'exp': int(exp_date.timestamp()),
        'type': type
    }
    if type in ['update_email']:
        payload['email'] = email
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def send_email(subject: str, template: tuple, context: dict, email: str):
    """Send a email to user email."""
    from_email = 'Sportfy <sportfy.com>'
    content = render_to_string(template, context)
    msg = EmailMultiAlternatives(subject, content, from_email, (email,))
    msg.attach_alternative(content, 'text/html')
    msg.send()
