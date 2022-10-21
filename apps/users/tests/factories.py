from typing import Any, Sequence

from apps.users.models import User
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """User model factory."""

    username = Faker('user_name')
    email = Faker('email')
    name = Faker('name')
    role = User.Role.athlete

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                'password',
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ['username']
