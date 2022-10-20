from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User
from taskapp.tasks import send_verification_email


@receiver(post_save, sender=User)
def verify_user_account(sender, instance, created, **kwargs):
    """Send a verification email to the created user."""
    if created:
        data = {
            'username': instance.username,
            'email': instance.email
        }
        send_verification_email.delay(user_data=data)
