import pytest

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status

# Models
from apps.users.models import User

pytestmark = pytest.mark.django_db


class TestUserCase:

    def test_user_signup(self, api_client):
        request_body = {
            'email': 'test@test.com',
            'username': 'usertest00',
            'first_name': 'First User',
            'last_name': 'First User',
            'phone_number': '+99 9999999999',
            'role': User.Role.athlete,
            'password': 'aipdsaapU',
            'password_confirmation': 'aipdsaapU'
        }
        response = api_client.post(reverse('users:users-signup'), request_body)
        user = User.objects.first()
        assert response.status_code == status.HTTP_201_CREATED
        assert user.username == 'usertest00'
