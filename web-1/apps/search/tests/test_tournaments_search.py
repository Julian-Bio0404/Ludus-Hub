import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestTournamentSearchCase:

    def test_list_tournament_search(self, athlete_client, api_client):
        url = reverse('search:tournaments-search')

        # Check authentication permission
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK
