"""Sports models."""

from apps.utils.files import sport_directory_path
from apps.utils.models import BaseAbstractModel, BaseModel
from django.db import models


class Sport(BaseModel):
    """Sport model."""

    description = models.TextField(blank=True)

    icon = models.ImageField(
        upload_to=sport_directory_path,
        blank=True,
        null=True
    )

    categories = models.ManyToManyField('sports.Category', blank=True)

    tags = models.ManyToManyField('sports.Tag', blank=True)

    def __str__(self) -> str:
        return self.name


class Rule(BaseAbstractModel):
    """Sport Rules model."""

    sport = models.ForeignKey('sports.Sport', on_delete=models.CASCADE)

    modality = models.ForeignKey('sports.Modality', on_delete=models.CASCADE)

    conditions = models.JSONField(default=dict)

    class Meta:
        unique_together = ('sport', 'modality')
