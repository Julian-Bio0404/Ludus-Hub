import json
import pytest

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from apps.users.models.users import User

# Factories
from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestProfileCase:

    def test_list_profiles(self, athlete_client, api_client):
        UserFactory(verified=True)
        UserFactory()
        url = reverse('users:profiles-list')

        # Check with unauth user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        content = json.loads(response.content)
        assert len(content['results']) == 1
        assert response.status_code == status.HTTP_200_OK

    def test_get_profile(self, athlete_client, api_client):
        user = UserFactory(verified=True)
        url = reverse('users:profiles-detail', args=[user.username])

        # Check with unauth user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_profile(self, athlete_client, trainer_client):
        user = athlete_client.user
        user.verified = True
        user.save()
        profile = user.profile
        url = reverse(
            'users:profiles-detail', args=[user.username])

        # Check with user owner of the profile
        body = {
            'first_name': 'Usertest',
            'profile': {
                'about': 'user test'
            }
        }
        response = athlete_client.patch(url, body, format='json')
        user_updated = User.objects.get(id=user.id)
        assert user.first_name != user_updated.first_name
        assert profile.about != user_updated.profile.about
        assert response.status_code == status.HTTP_200_OK

        # Check with only user data
        body = {'first_name': 'Usertest'}
        response = athlete_client.patch(url, body, format='json')
        assert response.status_code == status.HTTP_200_OK

        # Check with another user
        response = trainer_client.patch(url, body, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
