"""Profile models"""

# Django
from django.db import models

# Models
from apps.utils.models import SportfyModel

# Utils
from apps.utils.files import user_directory_path


class Profile(SportfyModel):
    """
    Profile model.
    Model One to one with User model.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    photo = models.ImageField(
        help_text='profile photo',
        upload_to=user_directory_path, blank=True, null=True)

    cover_photo = models.ImageField(
        help_text='profile cover photo',
        upload_to=user_directory_path, blank=True, null=True)

    about = models.TextField(
        help_text='write something about you', blank=True)

    birth_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)

    sport = models.CharField(
        help_text='What sport do you play?', max_length=25, blank=True)

    country = models.CharField(
        help_text='your country of origin', max_length=60, blank=True)

    public = models.BooleanField(help_text='Profile privacy', default=True)

    web_site = models.URLField(
        help_text='personal web site', max_length=200, blank=True)

    social_link = models.URLField(
        help_text='social media', max_length=200, blank=True)

    def __str__(self) -> str:
        return self.user.username
