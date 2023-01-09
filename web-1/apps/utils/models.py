"""Django models utilities."""

import uuid

from django.db import models


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
