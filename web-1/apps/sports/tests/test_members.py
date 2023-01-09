"""Members tests."""

from datetime import datetime, timedelta
import json

import pytest

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status

# Models
from apps.sports.models import Invitation, Member

# Factories
from apps.sports.tests.factories import (AssistanceFactory, ClubFactory,
                                         InvitationFactory, MemberFactory)

from apps.users.tests.factories import UserFactory

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


class TestInvitationCase:

    def test_create_invitation(self, trainer_client, athlete_client, api_client):
        club = ClubFactory(trainer=trainer_client.user)
        url = reverse('sports:invitations-list', args=[club.slug])
        invited = athlete_client.user.username
        body = {'invited': invited}

        # Check with another user
        response = athlete_client.post(url, body)
        invitations = Invitation.objects.filter(club=club)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert invitations.exists() is False

        # Check with club owner
        response = trainer_client.post(url, body)
        invitations = Invitation.objects.filter(club=club)
        assert response.status_code == status.HTTP_201_CREATED
        assert invitations.exists()

    def test_get_invitation(self, trainer_client, athlete_client, api_client):
        club = ClubFactory(trainer=trainer_client.user)
        invited = UserFactory()
        invitation = InvitationFactory(
            club=club, sent_by=trainer_client.user, invited=invited)
        url = reverse('sports:invitations-detail', args=[club.slug, invitation.id])

        # Check with another user
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with club owner
        response = trainer_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Check with invited user
        api_client.force_authenticate(user=invited)
        api_client.user = invited
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_invitation(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        InvitationFactory.create_batch(size=2, club=club, sent_by=trainer_client.user, used=True)
        InvitationFactory.create_batch(size=2, club=club, sent_by=trainer_client.user)
        url = reverse('sports:invitations-list', args=[club.slug])

        # Check with another user
        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with club owner
        response = trainer_client.get(url)
        content = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(content['results']) == 4

    def test_confirm_invitation(self, trainer_client, athlete_client, api_client):
        club = ClubFactory(trainer=trainer_client.user)
        invited = UserFactory()
        invitation = InvitationFactory(
            club=club, sent_by=trainer_client.user, invited=invited)
        url = reverse('sports:invitations-detail', args=[club.slug, invitation.id])
        body = {'used': True}
        invitation_db = Invitation.objects.get(invited=invited)

        # Check with another user
        response = athlete_client.patch(url, body)
        invitation_db.refresh_from_db()
        assert invitation_db.used == invitation.used
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with club owner
        response = trainer_client.patch(url, body)
        invitation_db.refresh_from_db()
        assert invitation_db.used == invitation.used
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with invited user
        api_client.force_authenticate(user=invited)
        api_client.user = invited
        response = api_client.patch(url, body)
        invitation_db.refresh_from_db()
        assert invitation_db.used != invitation.used
        assert response.status_code == status.HTTP_200_OK

    def test_delete_invitation(self, trainer_client, athlete_client, api_client):
        club = ClubFactory(trainer=trainer_client.user)
        invited = UserFactory()
        invitation = InvitationFactory(
            club=club, sent_by=trainer_client.user, invited=invited)
        url = reverse('sports:invitations-detail', args=[club.slug, invitation.id])

        # Check with another user
        response = athlete_client.delete(url)
        invitation_db = Invitation.objects.filter(invited=invited)
        assert invitation_db.exists()
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Check with club owner
        response = trainer_client.delete(url)
        invitation_db = Invitation.objects.filter(invited=invited)
        assert invitation_db.exists() is False
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check with invited user
        invitation2 = InvitationFactory(
            club=club, sent_by=trainer_client.user, invited=invited)
        url = reverse('sports:invitations-detail', args=[club.slug, invitation2.id])
        api_client.force_authenticate(user=invited)
        api_client.user = invited
        response = api_client.delete(url)
        invitation_db = Invitation.objects.filter(invited=invited)
        assert invitation_db.exists() is False
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestAssistanceCase:

    def test_create_asssitances(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        members = MemberFactory.create_batch(size=2, active=True, club=club)

        # other members and inactive members
        MemberFactory.create_batch(size=2, active=True)
        MemberFactory.create_batch(size=2, active=True, club=club)

        url = reverse('sports:assistances-list', args=[club.slug])
        body = {'members': [member.user.username for member in members]}

        response = trainer_client.post(url, body)
        content = json.loads(response.content)

        # Check that only create assistance by active club members
        assert response.status_code == status.HTTP_201_CREATED
        assert len(content[0]) == 2

        # Check with other user
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_asssitances(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        MemberFactory(active=True, club=club, user=athlete_client.user)
        assistance1 = AssistanceFactory(user=athlete_client.user, club=club)
        AssistanceFactory(user=athlete_client.user, club=club)

        date = datetime.now() - timedelta(days=1)
        assistance1.created = date
        assistance1.save()

        url = reverse('sports:assistances-list', args=[club.slug])
        response = trainer_client.get(url)
        content = json.loads(response.content)

        # Check that only list assitance of current day
        assert response.status_code == status.HTTP_200_OK
        assert content['count'] == 1

        member = athlete_client.user
        url = reverse('sports:members-assistances', args=[club.slug, member.username])
        response = athlete_client.get(url)
        content = json.loads(response.content)

        # Check that list all assistance of member
        assert response.status_code == status.HTTP_200_OK
        assert len(content['assistances']) == 2
