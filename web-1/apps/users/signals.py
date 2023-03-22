"""User signals."""

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# Tasks
from taskapp.tasks import send_verification_email

# Models
from apps.users.models import Profile, User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Set of actions executed after a user is created."""
    if created:
        data = {
            'username': instance.username,
            'email': instance.email
        }
        send_verification_email.delay(user_data=data)
        Profile.objects.create(user=instance)
