"""Subscription models."""

from apps.utils.models import SportfyModel
from django.db import models


class Subscription(SportfyModel):
    """Subscription model."""

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    plan = models.ForeignKey(
        'payments.Plan', on_delete=models.SET_NULL, null=True)

    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Subscription of {self.user.username}'
