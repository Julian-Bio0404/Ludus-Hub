"""Payments models."""

from apps.utils.models import SportfyModel
from django.db import models
from djchoices import ChoiceItem, DjangoChoices


class Price(SportfyModel):
    """Price model"""

    class Currency(DjangoChoices):
        """Price currency choices."""
        cop = ChoiceItem('cop', 'COP')
        usd = ChoiceItem('usd', 'USD')

    stripe_id = models.CharField(max_length=100, unique=True)

    currency = models.CharField(max_length=7, choices=Currency.choices)

    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.amount} - {self.currency}'
