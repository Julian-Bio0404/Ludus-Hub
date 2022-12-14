"""Club models."""

# Django
from django.db import models

# Utils
from apps.utils.models import SportfyModel


class Club(SportfyModel):
    """Club model."""

    name = models.CharField(max_length=150)

    slug = models.SlugField(unique=True, max_length=200)

    description = models.TextField(
        help_text='write about something', blank=True)

    web_site = models.URLField(
        help_text='Web site', max_length=150, blank=True)

    photo = models.ImageField(
        help_text='Club photo',
        upload_to='sports/clubs/photos%Y/%m/%d/', blank=True, null=True)

    cover_photo = models.ImageField(
        help_text='Club cover photo',
        upload_to='sports/clubs/cover_photos/%Y/%m/%d/', blank=True, null=True)

    city = models.CharField(
        help_text='State of the origin', max_length=60, blank=True)

    trainer = models.ForeignKey('users.User', on_delete=models.CASCADE)

    members = models.ManyToManyField(
        'users.User', through='sports.Member',
        through_fields=('club', 'user'), related_name='members')

    def __str__(self):
        """Return Club's slugname."""
        return self.slug
