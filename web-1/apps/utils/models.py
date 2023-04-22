"""Django models utilities."""

import uuid

from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.db import models


def custom_slugify(value):
    """Append sign + if needs."""
    position = value.find('+')
    sign = value[position] if position != -1 else None
    slug = slugify(value)
    if sign:
        return slug + sign
    return slug


class BaseSportfyModel(models.Model):
    """
    Base Sportfy Model.
    Acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following atribute:
        + id (UUIDField): Store id in uuid4 format
        + created (DateTime): Store the datetime the object was created.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    created = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created']


class SportfyModel(BaseSportfyModel):
    """
    Sportfy Model.
    Acts as an abstract base class inherits from
    BaseSportfyModel. Extend your models of this class to add
    the following field:
        + updated (DateTime): Store the datetime the object was updated.
    """

    updated = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-updated']


class SportModel(SportfyModel):
    """
    Sport Model.
    Acts as an abstract base class inherits from
    SportfyModel. Extend your models of this class to add
    the following field:
        + name (Charfield): Store the name the object.
        + slug (SlugField): Store the slug the object.
    """

    name = models.CharField(max_length=100)

    slug = AutoSlugField(
        max_length=150,
        populate_from='name',
        always_update=True
    )

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-updated', 'name']
