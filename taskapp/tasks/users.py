"""Users tasks."""

from __future__ import absolute_import, unicode_literals

# Utils
from apps.utils.email import send_email, token_generation

# Celery
from taskapp.celery import app


@app.task(bind=True)
def send_verification_email(self, user_data: dict) -> bool:
    """Send account verification link to given user."""
    username = user_data['username']
    token = token_generation(username, type='email_confirmation')
    email_data = {
        'subject': f"Welcome @{username}! Verify your account",
        'template': 'users/account_verification.html',
        'context': {'token': token, 'user': username},
        'email': user_data['email']
    }
    send_email(**email_data)
    return True


@app.task(bind=True)
def send_restore_password_email(self, user_data: dict) -> bool:
    """Send restore password link to given user."""
    username = user_data['username']
    token = token_generation(username, type='restore_password')
    email_data = {
        'subject': 'Update your password',
        'template': 'users/restore_password.html',
        'context': {'token': token, 'user': username},
        'email': user_data['email']
    }
    send_email(**email_data)
    return True


@app.task(bind=True)
def send_update_email(self, user_data: dict, email: str) -> bool:
    """Send update email link to given user."""
    username = user_data['username']
    token = token_generation(username, type='update_email', email=email)
    email_data = {
        'subject': f"Hi @{username}! Update your email",
        'template': 'users/update_email.html',
        'context': {'token': token, 'user': username},
        'email': user_data['email']
    }
    send_email(**email_data)
    return True
