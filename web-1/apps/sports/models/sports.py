"""Sports models."""

from apps.utils.files import sport_directory_path
from apps.utils.models import SportModel
from django.db import models


class Sport(SportModel):
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
