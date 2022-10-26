"""User models."""

# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Third party utils
from djchoices import ChoiceItem, DjangoChoices

# Models
from apps.utils.models import SportfyModel

# Utils
from apps.utils.files import user_directory_path


class User(SportfyModel, AbstractUser):
    """
    User model.
    Extend from Django's Abstract User and add some extra fields.
    """

    class Role(DjangoChoices):
        """User role choices."""
        athlete = ChoiceItem('athlete', 'Athlete')
        trainer = ChoiceItem('trainer', 'Trainer')

    email = models.EmailField(
        'email address', unique=True,
        error_messages={'unique': 'A user with that email already exists.'})

    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)

    verified = models.BooleanField(
        default=False, help_text='Set to true when the user have verified its email add')

    role = models.CharField(
        help_text='role of user.', max_length=16, choices=Role.choices)

    # Username configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username


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

    def __str__(self):
        return self.user.username
