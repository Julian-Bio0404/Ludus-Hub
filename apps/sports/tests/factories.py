"""Club factories."""

from typing import Any, Sequence

from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

# Models
from apps.sports.models import Club, Invitation, Member

# Factories
from apps.users.tests.factories import UserFactory


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
