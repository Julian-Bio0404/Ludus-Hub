import pytest

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status

# Models
from apps.users.models import Profile, User

# Factories
from apps.users.tests.factories import UserFactory

# Utils
from apps.utils.email import token_generation

pytestmark = pytest.mark.django_db


class TestUserCase:

    def test_user_signup(self, api_client):
        body = {
            'email': 'test@test.com',
            'username': 'usertest',
            'first_name': 'First User',
            'last_name': 'First User',
            'phone_number': '+99 9999999999',
            'role': User.Roles.athlete,
            'password': 'aipdsaapU',
            'password_confirmation': 'aipdsaapU'
        }
        url = reverse('users:users-signup')
        # Check with invalid phone number
        body1 = body.copy()
        body1['phone_number'] = '99999999'
        response = api_client.post(url, body1)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with invalid role
        body2 = body.copy()
        body2['role'] = 'xxxxxxxxxx'
        response = api_client.post(url, body2)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with password != password_confirmation
        body3 = body.copy()
        body3['password'] = 'aipdsaapU'
        body3['password_confirmation'] = 'aipdsaapO'
        response = api_client.post(url, body3)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with already existing username
        user2 = UserFactory(username='usertest01')
        body4 = body.copy()
        body4['username'] = user2.username
        response = api_client.post(url, body4)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with already existing email
        body5 = body.copy()
        body5['email'] = user2.email
        response = api_client.post(url, body5)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check signup sucess
        response = api_client.post(url, body)
        user = User.objects.get(username='usertest')
        Profile.objects.get(user=user)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_verification(self, athlete_client):
        url = reverse('users:users-verify')
        assert athlete_client.user.verified is False

        # Check with invalid token
        body = {'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        response = athlete_client.post(url, body)
        user = User.objects.get(username=athlete_client.user.username)
        assert user.verified is False
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with invalid type token
        token = token_generation(
            username=athlete_client.user.username, type='update_email')
        body = {'token': token}
        response = athlete_client.post(url, body)
        user.refresh_from_db(fields=['verified'])
        assert user.verified is False
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with valid token
        token = token_generation(
            username=athlete_client.user.username, type='email_confirmation')
        body = {'token': token}
        response = athlete_client.post(url, body)
        user.refresh_from_db(fields=['verified'])
        assert user.verified
        assert response.status_code == status.HTTP_200_OK

    def test_user_login(self, api_client):
        body = {
            'email': 'test04@gmail.com',
            'username': 'test04',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': User.Roles.athlete,
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW_'
        }
        api_client.post(reverse('users:users-signup'), body)
        url = reverse('users:users-login')

        # Check with unverified user
        user = User.objects.get(username='test04')
        body = {
            'email': user.email,
            'password': 'nKSAJBBCJW_'
        }
        response = api_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check with verified user
        user.verified = True
        user.save()
        response = api_client.post(url, body)
        assert response.status_code == status.HTTP_201_CREATED

        # Check with wrong password
        body['password'] = 'nKSAJBBCJW'
        response = api_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_password(self, api_client):
        """Verifies that update password is success."""
        user = User.objects.create_user(
            username='usertest00',
            first_name='First test',
            last_name='First test',
            email='test@test.com',
            role='athlete',
            verified=True,
            password='6iu8989buy79'
        )
        api_client.force_authenticate(user=user)
        url = reverse('users:users-update-psswd', args=[user.username])

        # Check with password != old password
        body = {
            'old_password': '6iu8989buy79',
            'password': '6iu8989buy7',
            'password_confirmation': 'prueba1234'
        }
        response = api_client.put(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check wrong password.
        body['old_password'] = 'admin1234'
        response = api_client.put(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Success
        body['old_password'] = '6iu8989buy79'
        body['password_confirmation'] = '6iu8989buy7'
        response = api_client.put(url, body)
        assert response.status_code == status.HTTP_200_OK

        body = {
            'email': user.email,
            'password': '6iu8989buy7'
        }
        response = api_client.post(reverse('users:users-login'), body)
        assert response.status_code == status.HTTP_201_CREATED

    def test_restore_psswd_token(self, athlete_client):
        url = reverse('users:users-token-restore-psswd')
        body = {'email': athlete_client.user.email}
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_200_OK

        # Check with user that does not exist
        body['email'] = 'prueba@p.com'
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_restore_password(self, athlete_client):
        # Check invalid token
        url = reverse('users:users-restore-psswd')
        body = {
            'password': 'knjxlksjbda',
            'password_confirmation': 'knjxlksjbda',
            'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        }
        response = athlete_client.post(url, body)
        user = User.objects.get(username=athlete_client.user.username)
        assert athlete_client.user.password == user.password
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check invalid token type
        token = token_generation(
            username=athlete_client.user.username, type='update_email')
        body = {
            'password': 'knjxlksjbda',
            'password_confirmation': 'knjxlksjbda',
            'token': token
        }
        response = athlete_client.post(url, body)
        assert athlete_client.user.password == user.password
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Success
        token = token_generation(
            username=athlete_client.user.username, type='restore_password')
        body = {
            'password': 'knjxlksjbda',
            'password_confirmation': 'knjxlksjbda',
            'token': token
        }
        response = athlete_client.post(url, body)
        user.refresh_from_db(fields=['password'])
        assert athlete_client.user.password != user.password
        assert response.status_code == status.HTTP_200_OK

    def test_update_email_token(self, api_client):
        user = UserFactory(password='admin123')
        api_client.user = user
        api_client.force_authenticate(user=user)

        body = {
            'new_email': 'test2@gmail.com',
            'password': 'admin123'
        }
        url = reverse(
            'users:users-token-update-email', args=[user.username])
        response = api_client.post(url, body)
        print(response.content)
        assert response.status_code == status.HTTP_200_OK

    def test_update_user_email(self, athlete_client):

        user = athlete_client.user

        # Invalid token type
        token = token_generation(
            username=user.username, type='email_confirmation', email='update@email.com')
        body = {
            'new_email': 'update@email.com',
            'token': token,
            'password': 'admin123'
        }
        url = reverse('users:users-update-email')
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # With invalid token
        body = {
            'new_email': 'update@email.com',
            'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'password': 'admin123'
        }
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # New Email != token email
        token = token_generation(
            username=user.username, type='update_email', email='update@email.com')
        body = {
            'new_email': 'updatlkjle2@email.com',
            'token': token,
            'password': 'admin123'
        }
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Wrong password
        token = token_generation(
            username=user.username, type='update_email', email='update@email.com')
        body = {
            'new_email': 'update@email.com',
            'token': token,
            'password': 'xxxxxxxxxxxxx'
        }
        response = athlete_client.post(url, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Success
        token = token_generation(
            username=user.username, type='update_email', email='update@email.com')
        body = {
            'new_email': 'update@email.com',
            'token': token,
            'password': 'admin123'
        }
        response = athlete_client.post(url, body)
        db_user = User.objects.get(username=user.username)
        assert user.email != db_user.email
        assert response.status_code == status.HTTP_200_OK
