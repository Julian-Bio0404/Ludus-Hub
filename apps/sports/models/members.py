"""Member models."""

# Django
from django.db import models

# Utils
from apps.utils.models import SportfyModel


class Member(SportfyModel):
    """
    Member model.
    A member is intermadiate model between
    user and a club.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        """Return username and club."""
        return f'@{self.user.username} at {self.club.slug}'
