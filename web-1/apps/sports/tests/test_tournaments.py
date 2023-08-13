import json
from datetime import datetime, timedelta

import pytest
from apps.sports.models import Tournament
from apps.sports.tests.factories import (CategoryFactory, SportFactory,
                                         TournamentFactory)
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestTournamentCase:

    def test_list_tournaments(self, athlete_client, api_client):
        TournamentFactory.create_batch(size=3)
        url = reverse('sports:tournaments-list')

        # Check with unauth user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        content = json.loads(response.content)
        assert len(content['results']) == 3
        assert response.status_code == status.HTTP_200_OK

    def test_get_tournament(self, athlete_client, api_client):
        tournament = TournamentFactory()
        url = reverse('sports:tournaments-detail', args=[tournament.id])

        # Check with unauth user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_tournament(self, trainer_client, api_client):
        url = reverse('sports:tournaments-list')
        sport = SportFactory(name='Karate')
        category = CategoryFactory(name='Senior: Kata')
        date = datetime.now() + timedelta(days=60)

        body = {
            'name': 'tournament test',
            'type': 'tournament-test',
            'level': 'tournament-test',
            'sport': 'Karate',
            'date': date

        }

        # Check with unauth user
        response = api_client.post(url, body, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with athlete user with bad request
        response = trainer_client.post(url, body, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with auth user without sport category
        body2 = {
            'name': 'tournament test',
            'type': Tournament.Types.qualifying,
            'level': Tournament.Levels.national,
            'sport': 'Karate',
            'date': date,
            'city': 'Neiva',
            'address': 'Cll Siempre Viva',
            'categories': [category.id]
        }
        response = trainer_client.post(url, body2, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with auth user
        sport.categories.add(category)

        body3 = {
            'name': 'tournament test',
            'type': Tournament.Types.qualifying,
            'level': Tournament.Levels.national,
            'sport': 'Karate',
            'date': date,
            'city': 'Neiva',
            'address': 'Cll Siempre Viva',
            'categories': [category.id]
        }
        response = trainer_client.post(url, body3, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_tournament(self, trainer_client, athlete_client):
        tournament = TournamentFactory(creator=athlete_client.user)
        url = reverse('sports:tournaments-detail', args=[tournament.id])

        # Check with another user
        response = trainer_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with owner user
        response = athlete_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
