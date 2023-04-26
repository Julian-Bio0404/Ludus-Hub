import json

import pytest
from apps.sports.models import Club
from apps.sports.tests.factories import ClubFactory, SportFactory
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestClubsCase:

    def test_list_clubs(self, athlete_client, api_client):
        ClubFactory.create_batch(size=3)
        url = reverse('sports:clubs-list')

        # Check with unauth user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        content = json.loads(response.content)
        assert len(content['results']) == 3
        assert response.status_code == status.HTTP_200_OK

    def test_get_club(self, athlete_client, api_client):
        club = ClubFactory()
        url = reverse('sports:clubs-detail', args=[club.slug])

        # Check with unauth user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_club(self, trainer_client, athlete_client, api_client):
        body = {
            'name': 'Club test',
            'slug': 'Club-test',
            'sport': 'Karate'
        }
        url = reverse('sports:clubs-list')

        # Check with unauth user
        response = api_client.post(url, body, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with athlete user
        response = athlete_client.post(url, body, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with trainer user and without sport
        response = trainer_client.post(url, body, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # Check with sport
        body2 = {
            'name': 'Club test2',
            'slug': 'Club-test2',
            'sport': 'Karate'
        }
        sport = SportFactory(name='Karate')
        response = trainer_client.post(url, body2, format='json')
        content = json.loads(response.content)
        assert response.status_code == status.HTTP_201_CREATED
        assert content['sport'] == sport.name

    def test_update_club(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        body = {
            'description': 'description test',
            'sport': 'Karate'
        }
        SportFactory(name='Karate')
        url = reverse('sports:clubs-detail', args=[club.slug])

        # Check with another user
        response = athlete_client.patch(url, body, format='json')
        club_edited = Club.objects.get(id=club.id)
        assert club.description == club_edited.description
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with owner user
        response = trainer_client.patch(url, body, format='json')
        club_edited = Club.objects.get(id=club.id)
        assert club.description != club_edited.description
        assert club.sport != club_edited.sport
        assert response.status_code == status.HTTP_200_OK

    def test_delete_club(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        url = reverse('sports:clubs-detail', args=[club.slug])

        # Check with another user
        response = athlete_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with owner user
        response = trainer_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
