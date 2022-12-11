"""Members tests."""

import json
import pytest

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status

# Models
from apps.sports.models import Member

# Factories
from apps.sports.tests.factories import ClubFactory, MemberFactory

pytestmark = pytest.mark.django_db


class TestMembersCase:

    def test_list_club_members(self, athlete_client, api_client):
        club = ClubFactory()
        MemberFactory.create_batch(size=2, active=True, club=club)
        MemberFactory(club=club)
        url = reverse('sports:members-list', args=[club.slug])

        # Check with anonymous user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        content = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(content['results']) == 3

    def test_get_club_member(self, athlete_client, api_client):
        club = ClubFactory()
        member = MemberFactory(club=club, active=True)
        user = member.user
        url = reverse('sports:members-detail', args=[club.slug, user.username])

        # Check with anonymous user
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Check with auth user
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_expel_club_member(self, athlete_client, trainer_client):
        club = ClubFactory(trainer=trainer_client.user)
        member = MemberFactory(club=club, active=True)
        user = member.user
        url = reverse('sports:members-detail', args=[club.slug, user.username])

        # Check with another user
        response = athlete_client.delete(url)
        members = club.members.all()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert members.count() == 1

        # Check with club trainer
        response = trainer_client.delete(url)
        members = club.members.all()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert members.count() == 0

    def test_exit_of_club(self, athlete_client):
        user = athlete_client.user
        club = ClubFactory()
        MemberFactory(club=club, active=True, user=user)
        url = reverse('sports:members-detail', args=[club.slug, user.username])
        response = athlete_client.delete(url)
        members = club.members.all()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert members.count() == 0

    def test_inactive_member(self, trainer_client, athlete_client):
        trainer = trainer_client.user
        club = ClubFactory(trainer=trainer)
        member = MemberFactory(club=club, active=True)
        user = member.user
        url = reverse('sports:members-detail', args=[club.slug, user.username])
        body = {'active': False}

        # Check with another user
        response = athlete_client.patch(url, body)
        member = Member.objects.get(user=user)
        assert member.active
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with club owner
        response = trainer_client.patch(url, body)
        member.refresh_from_db()
        assert member.active is False
        assert response.status_code == status.HTTP_200_OK
