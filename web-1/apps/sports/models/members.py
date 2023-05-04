"""Member models."""

from apps.utils.models import BaseSportfyModel, SportfyModel, SportModel
from django.db import models


class Member(SportfyModel):
    """
    Member model.
    A member is intermadiate model between
    user and a club.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)

    active = models.BooleanField(default=False)

    def all_assistances(self) -> int:
        return self.club.assistance_set.filter(user=self.user).count()

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


class Team(SportModel):
    """
    Team model.
    A team is a group of athletes of a club.
    """

    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)

    users = models.ManyToManyField('users.User', blank=True)

    category = models.ForeignKey(
        'sports.Category', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        """Return team name."""
        return self.name
