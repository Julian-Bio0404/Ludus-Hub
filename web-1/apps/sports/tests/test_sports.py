import json

import pytest
from apps.sports.tests.factories import (CategoryFactory, ModalityFactory,
                                         SportFactory)
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestSportCase:

    def test_list_sports(self, athlete_client, api_client):
        modality = ModalityFactory(name='Kata')
        category1 = CategoryFactory(modality=modality, name='Senior')
        SportFactory(categories=[category1])
        url = reverse('sports:sports-list')
        response = api_client.get(url)
        content = json.loads(response.content)
        assert len(content['results']) == 1
        assert len(content['results'][0]['categories']) == 1
        assert response.status_code == status.HTTP_200_OK

    def test_sport_detail(self, athlete_client, api_client):
        modality = ModalityFactory(name='Kata')
        category1 = CategoryFactory(modality=modality, name='Senior')
        sport = SportFactory(categories=[category1])
        url = reverse('sports:sports-detail',  args=[sport.id])
        response = api_client.get(url)
        content = json.loads(response.content)
        assert len(content['categories']) == 1
        assert response.status_code == status.HTTP_200_OK
