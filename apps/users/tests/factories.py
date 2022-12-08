# Utilities
from typing import Any, Sequence
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

# Models
from apps.users.models import User


class UserFactory(DjangoModelFactory):
    """User model factory."""

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('name')
    last_name = Faker('name')
    role = User.Roles.athlete

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = extracted if extracted else 'admin123'
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ['username']
