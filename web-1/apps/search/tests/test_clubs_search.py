import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestClubSearchCase:

    def test_list_club_search(self, athlete_client, api_client):
        url = reverse('search:clubs-search')
        response = athlete_client.get(url)
        # content = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
