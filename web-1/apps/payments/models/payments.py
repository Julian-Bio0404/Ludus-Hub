"""Payments models."""

import re

from apps.utils.models import BaseAbstractModel
from django.core.validators import RegexValidator
from django.db import models
from djchoices import ChoiceItem, DjangoChoices


class Price(BaseAbstractModel):
    """Price model"""

    class Currency(DjangoChoices):
        """Price currency choices."""
        cop = ChoiceItem('cop', 'COP')
        usd = ChoiceItem('usd', 'USD')

    stripe_id = models.CharField(max_length=100, unique=True)

    currency = models.CharField(max_length=7, choices=Currency.choices)

    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def dissociate_amount(self) -> tuple[int, int]:
        """Return digits and decimal amount."""
        match = re.match(r'^(\d{1,7})\.(\d{2})$', str(self.amount))
        return int(match.group(1)), int(match.group(2))

    def __str__(self) -> str:
        return f'{self.amount} - {self.currency}'


class Card(BaseAbstractModel):
    """Customer Card model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    stripe_id = models.CharField(max_length=100, unique=True)

    last4_regex = RegexValidator(
        regex=r"^\d{4}$",
        message='last4 number must be 4 digits.')

    last4 = models.CharField(validators=[last4_regex], max_length=4, blank=True)

    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.last4}'
