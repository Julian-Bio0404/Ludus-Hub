import pytest

# Django REST Framework
from rest_framework.test import APIClient

# Models
from apps.users.models import User

# Factories
from apps.users.tests.factories import UserFactory


@pytest.fixture(scope='function')
def athlete_user() -> User:
    """Create fake athlete user."""
    return UserFactory()


@pytest.fixture(scope='function')
def trainer_user() -> User:
    """Create fake trainer user."""
    return UserFactory(role=User.Role.trainer)


@pytest.fixture(scope='function')
def athlete_client(athlete_user) -> APIClient:
    """Create auth client with athlete user."""
    client = APIClient()
    client.force_authenticate(user=athlete_user)
    client.user = athlete_user
    return client


@pytest.fixture(scope='function')
def trainer_client(trainer_user) -> APIClient:
    """Create auth client with trainer user."""
    client = APIClient()
    client.force_authenticate(user=trainer_user)
    client.user = trainer_user
    return client


@pytest.fixture(scope='function')
def api_client(trainer_user) -> APIClient:
    """Anonymous client."""
    client = APIClient()
    return client
