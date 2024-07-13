from datetime import datetime

from factory import Factory, Faker, LazyFunction, SubFactory
from app.models.clubs import Club, Member
from app.models.users import Token, User


class UserFactory(Factory):
    """User model factory."""

    id = Faker('uuid4')
    username = Faker('user_name')

    class Meta:
        model = User


class TokenFactory(Factory):
    """Token model factory."""

    key = Faker('uuid4')
    user = SubFactory(UserFactory)
    created = LazyFunction(datetime.now)

    class Meta:
        model = Token


class ClubFactory(Factory):
    """Club model factory."""

    id = Faker('uuid4')
    slug = Faker('slug')
    name = Faker('name')

    class Meta:
        model = Club


class MemberFactory(Factory):
    """Member model factory."""

    id = Faker('uuid4')
    user = SubFactory(UserFactory)
    club = SubFactory(ClubFactory)
    active = Faker('boolean')

    class Meta:
        model = Member
