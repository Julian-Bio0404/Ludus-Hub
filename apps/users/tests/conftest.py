import pytest
from apps.users.models import User
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIClient


@pytest.fixture
def user() -> User:
    """Create fake user."""
    return UserFactory()


@pytest.fixture
def api_client(user) -> APIClient:
    """Create auth client."""
    client = APIClient()
    client.force_authenticate(user=user)
    client.user = user
    return client
