"""Members tests."""

import json
from datetime import datetime, timedelta

import pytest
from apps.sports.models import Invitation, Member, Team
from apps.sports.tests.factories import (AssistanceFactory, ClubFactory,
                                         InvitationFactory, MemberFactory,
                                         TeamFactory, CategoryFactory, SportFactory)
from apps.users.tests.factories import UserFactory
from django.urls import reverse
from rest_framework import status

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


class TestTeamCase:

    def test_create_team(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        url = reverse('sports:teams-list', args=[club.slug])

        # Create with user that not is trainer
        body = {'name': 'team test 1', 'category': 'Senior'}
        response = athlete_client.post(url, body)
        team = Team.objects.filter(name='team test 1')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not team.exists()

        # Create wiht category that does not exist
        body = {'name': 'team test 1', 'category': 'Senior'}
        response = trainer_client.post(url, body)
        team = Team.objects.filter(name='team test 1')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not team.exists()

        # Create with category that exist but the club don't have a category
        category = CategoryFactory(name='Female Senior')
        body = {'name': 'team test 1', 'category': category.id}
        response = trainer_client.post(url, body)
        team = Team.objects.filter(name='team test 1')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not team.exists()

        # Create without category and members
        body = {'name': 'team test 1'}
        response = trainer_client.post(url, body)
        team = Team.objects.filter(name='team test 1')
        assert response.status_code == status.HTTP_201_CREATED
        assert team.exists()

        # Create with category and the club have the category
        sport = SportFactory(name='Karate')
        sport.categories.add(category)
        club.sport = sport
        club.save()
        body = {'name': 'team test 2', 'category': category.id}
        response = trainer_client.post(url, body)
        team = Team.objects.filter(name='team test 2')
        assert response.status_code == status.HTTP_201_CREATED
        assert team.exists()

        # Create with users that are not members of club
        body = {'name': 'team test 3', 'users': [athlete_client.user.username]}
        response = trainer_client.post(url, body)
        team = Team.objects.filter(name='team test 3')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not team.exists()

        # Create with users that are members of club
        MemberFactory(active=True, club=club, user=athlete_client.user)
        body = {'name': 'team test 3', 'users': [athlete_client.user.username]}
        response = trainer_client.post(url, body)
        team = Team.objects.filter(name='team test 3')
        assert response.status_code == status.HTTP_201_CREATED
        assert team.exists()

    def test_add_member(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        team = TeamFactory(club=club)
        url = reverse('sports:teams-add-member', args=[club.slug, team.id])

        # with users that are not members of club
        body = {'users': [athlete_client.user.username]}
        response = trainer_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # with users that are members of club
        MemberFactory(active=True, club=club, user=athlete_client.user)
        body = {'users': [athlete_client.user.username]}
        response = trainer_client.post(url, body)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_member(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        team = TeamFactory(club=club)
        url = reverse('sports:teams-remove-member', args=[club.slug, team.id])
        MemberFactory(active=True, club=club, user=athlete_client.user)
        body = {'users': [athlete_client.user.username]}
        response = trainer_client.post(url, body)
        assert response.status_code == status.HTTP_200_OK

    def test_update_team(self, trainer_client, athlete_client):
        category = CategoryFactory(name='Female Senior')
        sport = SportFactory(name='Karate', categories=[category])
        club = ClubFactory(trainer=trainer_client.user, sport=sport)
        team = TeamFactory(club=club)
        # sport.categories.add(category)
        url = reverse('sports:teams-detail', args=[club.slug, team.id])

        # Update with club admin
        body = {'name': 'team test 1', 'category_id': category.id}
        response = trainer_client.patch(url, body)
        team_update = Team.objects.get(id=team.id)
        assert response.status_code == status.HTTP_200_OK
        assert team.name != team_update.name
        assert team.category != team_update.category

        # Update with category that does not belong to club sport
        category2 = CategoryFactory(name='Basic Senior')
        body = {'name': 'team test 1', 'category_id': category2.id}
        response = trainer_client.patch(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Update with athlete user
        body = {'name': 'team test 2'}
        response = athlete_client.patch(url, body)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_team(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        team = TeamFactory(club=club)
        url = reverse('sports:teams-detail', args=[club.slug, team.id])
        response = trainer_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_teams(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        TeamFactory.create_batch(size=3, club=club)
        url = reverse('sports:teams-list', args=[club.slug])
        response = trainer_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = athlete_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def delete_team(self, trainer_client, athlete_client):
        club = ClubFactory(trainer=trainer_client.user)
        team = TeamFactory(club=club)
        url = reverse('sports:teams-detail', args=[club.slug, team.id])
        response = athlete_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = trainer_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
