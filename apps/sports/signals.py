"""Club signals."""

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from apps.sports.models import Club
from apps.chat.models import Room


@receiver(post_save, sender=Club)
def club_post_save(sender, instance, created, **kwargs):
    """Set of actions executed after a club is created."""
    if created:
        room = Room.objects.create(club=instance, slug=instance.slug)
        room.receivers.add(instance.trainer)
