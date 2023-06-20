"""Plan models."""

from apps.utils.models import BaseAbstractModel
from django.db import models
from djchoices import ChoiceItem, DjangoChoices


class Plan(BaseAbstractModel):
    """Plan model."""

    class Intervals(DjangoChoices):
        """Plan type choices."""
        month = ChoiceItem('month', 'Month')
        year = ChoiceItem('year', 'Year')

    stripe_id = models.CharField(max_length=100, unique=True)

    product_id = models.CharField(max_length=100, unique=True, null=True)

    name = models.CharField(max_length=20, unique=True)

    interval = models.CharField(max_length=7, choices=Intervals.choices)

    price = models.ForeignKey('payments.Price', on_delete=models.PROTECT)

    description = models.TextField(max_length=300, blank=True)

    def __str__(self) -> str:
        return f'{self.interval}: ${self.price}'
