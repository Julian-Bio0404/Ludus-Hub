"""Club signals."""

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from apps.chat.models import Room
from apps.sports.models import Club, Member


@receiver(post_save, sender=Club)
def club_post_save(sender, instance, created, **kwargs):
    """Set of actions executed after a club is created."""
    if created:
        room = Room.objects.create(club=instance, slug=instance.slug)
        room.receivers.add(instance.trainer)


@receiver(post_save, sender=Member)
def member_post_save(sender, instance, created, **kwargs):
    """Set of actions executed after a member joins the club."""
    if created:
        room = instance.club.room
        room.receivers.add(instance.user)
