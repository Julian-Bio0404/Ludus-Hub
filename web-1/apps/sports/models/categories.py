"""Categories models."""

from apps.utils.models import SportModel, custom_slugify
from autoslug import AutoSlugField
from django.db import models
from djchoices import ChoiceItem, DjangoChoices


class Modality(SportModel):
    """Modality model."""

    class Meta:
        verbose_name_plural = 'Modalities'

    def __str__(self) -> str:
        return self.name


class Category(SportModel):
    """Category model."""

    class Gender(DjangoChoices):
        """Gender Types."""
        male = ChoiceItem('male', 'Male')
        female = ChoiceItem('female', 'Female')
        mixed = ChoiceItem('mixed', 'Mixed')

    slug = AutoSlugField(
        populate_from='name',
        unique_with=['name', 'gender', 'modality'],
        always_update=True,
        slugify=custom_slugify
    )

    gender = models.CharField(choices=Gender.choices, max_length=6)

    modality = models.ForeignKey(
        'sports.Modality',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['slug']

    def __str__(self) -> str:
        if self.modality:
            return f'{self.modality}: {self.name}-{self.gender}'
        return f'{self.name}-{self.gender}'


class Tag(SportModel):
    """Tag model."""

    def __str__(self) -> str:
        return self.name
