"""Room models."""

# Django
from django.db import models

# Utils
from apps.utils.models import BaseSportfyModel


class Room(BaseSportfyModel):
    """Room model."""

    slug = models.SlugField(unique=True, max_length=200)
    club = models.OneToOneField('sports.Club', on_delete=models.CASCADE)
    receivers = models.ManyToManyField('users.User', related_name='receivers')

    def __str__(self) -> str:
        """Return room's slug."""
        return self.slug
