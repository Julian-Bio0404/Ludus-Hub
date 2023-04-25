"""Club factories."""

from typing import Any, Sequence

from apps.sports.models import (Assistance, Category, Club, Invitation, Member,
                                Modality, Sport, Tag)
from apps.users.tests.factories import UserFactory
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory


class ClubFactory(DjangoModelFactory):
    """Club model factory."""

    trainer = SubFactory(UserFactory)
    name = Faker('company')
    slug = Faker('slug')

    @post_generation
    def members(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.members.set(extracted)

    class Meta:
        model = Club
        django_get_or_create = ['slug']


class MemberFactory(DjangoModelFactory):
    """Member model factory."""

    user = SubFactory(UserFactory)
    club = SubFactory(ClubFactory)

    class Meta:
        model = Member


class InvitationFactory(DjangoModelFactory):
    """Invitation model factory."""

    sent_by = SubFactory(UserFactory)
    invited = SubFactory(UserFactory)
    club = SubFactory(ClubFactory)

    class Meta:
        model = Invitation


class AssistanceFactory(DjangoModelFactory):
    """Assistance model factory."""

    user = SubFactory(UserFactory)
    club = SubFactory(ClubFactory)

    class Meta:
        model = Assistance


class SportFactory(DjangoModelFactory):
    """Sport model factory."""

    name = Faker('company')

    @post_generation
    def categories(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.categories.set(extracted)

    @post_generation
    def tags(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.tags.set(extracted)

    class Meta:
        model = Sport
        django_get_or_create = ['name']


class ModalityFactory(DjangoModelFactory):
    """Modality model factory."""

    name = Faker('company')

    class Meta:
        model = Modality
        django_get_or_create = ['name']


class CategoryFactory(DjangoModelFactory):
    """Category model factory."""

    name = Faker('company')
    modality = SubFactory(ModalityFactory)
    genre = Category.Genders.female

    class Meta:
        model = Category
        django_get_or_create = ['name']


class TagFactory(DjangoModelFactory):
    """Tag model factory."""

    name = Faker('company')

    class Meta:
        model = Tag
        django_get_or_create = ['name']
