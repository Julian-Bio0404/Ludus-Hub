"""Plan models."""

from apps.utils.models import SportfyModel
from django.db import models
from djchoices import ChoiceItem, DjangoChoices


class Plan(SportfyModel):
    """Plan model."""

    class Types(DjangoChoices):
        """Plan type choices."""
        monthly = ChoiceItem('monthly', 'Monthly')
        annual = ChoiceItem('annual', 'Annual')

    type = models.CharField(max_length=7, choices=Types.choices)

    price = models.ForeignKey('payments.Price', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.type}: ${self.price}'
