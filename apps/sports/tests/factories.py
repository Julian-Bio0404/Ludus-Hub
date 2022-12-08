"""Club factories."""

from typing import Any, Sequence
from factory.django import DjangoModelFactory
from factory import SubFactory, Faker, post_generation

# Models
from apps.sports.models import Club

# Factories
from apps.users.tests.factories import UserFactory


class ClubFactory(DjangoModelFactory):
    """Club model factory."""

    trainer = SubFactory(UserFactory)
    name = Faker('company')
    slug = Faker('name')

    @post_generation
    def members(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.members.set(extracted)

    class Meta:
        model = Club
        django_get_or_create = ['slug']
