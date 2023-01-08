"""Member models."""

# Django
from django.db import models

# Utils
from apps.utils.models import SportfyModel, BaseSportfyModel


class Member(SportfyModel):
    """
    Member model.
    A member is intermadiate model between
    user and a club.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return username and club."""
        return f'@{self.user.username} at {self.club.slug}'


class Invitation(SportfyModel):
    """Invitation model."""

    sent_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

    invited = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='invited')

    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return club and athlete."""
        return f'{self.sent_by} from {self.club}: {self.invited}'


class Assistance(BaseSportfyModel):
    """Assistance model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return club and athlete."""
        return f'{self.user.username} at: {self.created}'
