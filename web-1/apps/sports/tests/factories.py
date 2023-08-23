"""Sport factories."""

from datetime import datetime, timedelta
from typing import Any, Sequence

from apps.sports.models import (Assistance, Category, Club, Competitor,
                                Invitation, Member, Modality, Sport, Tag, Team,
                                Tournament)
from apps.users.tests.factories import UserFactory
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyNaiveDateTime


class SportFactory(DjangoModelFactory):
    """Sport model factory."""

    name = Faker('company')

    @post_generation
    def categories(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.categories.add(*extracted)

    @post_generation
    def tags(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.tags.add(*extracted)

    class Meta:
        model = Sport
        django_get_or_create = ['name']


class ClubFactory(DjangoModelFactory):
    """Club model factory."""

    trainer = SubFactory(UserFactory)
    name = Faker('company')
    slug = Faker('slug')
    sport = SubFactory(SportFactory)

    @post_generation
    def members(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.members.add(*extracted)

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
    gender = Category.Genders.female

    class Meta:
        model = Category
        django_get_or_create = ['name']


class TagFactory(DjangoModelFactory):
    """Tag model factory."""

    name = Faker('company')

    class Meta:
        model = Tag
        django_get_or_create = ['name']


class TeamFactory(DjangoModelFactory):
    """Team model factory."""

    name = Faker('company')
    club = SubFactory(ClubFactory)

    class Meta:
        model = Team


class TournamentFactory(DjangoModelFactory):
    """Tournament model factory."""

    creator = SubFactory(UserFactory)
    name = Faker('company')
    type = Tournament.Types.open
    level = Tournament.Levels.local
    sport = SubFactory(SportFactory)
    date = FuzzyNaiveDateTime(
        datetime.now(),
        datetime.now() + timedelta(days=365)
    )

    @post_generation
    def categories(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        if extracted:
            self.categories.add(*extracted)

    class Meta:
        model = Tournament


class BaseCompetitorFactory(DjangoModelFactory):
    """Base Competitor factory."""

    category = SubFactory(CategoryFactory)
    tournament = SubFactory(TournamentFactory)

    class Meta:
        model = Competitor


class AthleteCompetitorFactory(BaseCompetitorFactory):
    """Competitor model factory."""

    athlete = SubFactory(UserFactory)


class TeamCompetitorFactory(BaseCompetitorFactory):
    """Competitor model factory."""

    team = SubFactory(TeamFactory)
