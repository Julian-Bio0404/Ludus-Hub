"""Users views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Serializers
from apps.users.serializers import (AccountVerificationSerializer,
                                    RestorePasswordSerializer,
                                    TokenRestorePasswordSerializer,
                                    TokenUpdateEmailSerializers,
                                    UpdateEmailSerializers,
                                    UpdatePasswordSerializer,
                                    UserLoginSerializer, UserModelSerializer,
                                    UserSignUpSerializer)


class UserViewSet(viewsets.GenericViewSet):
    """
    User view set.
    Handle signup, login, account
    verification update and restore password.
    """

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action == 'update_psswd':
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, your account has been verified!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_psswd(self, request, *args, **kwargs):
        """Update user's password."""
        serializer = UpdatePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your password has been updated.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def token_restore_psswd(self, request):
        """Create a token for restore password."""
        serializer = TokenRestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We have sent an email for you to reset your password.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def restore_psswd(self, request):
        """Restore user's password."""
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your password has been reset.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def token_update_email(self, request, *args, **kwargs):
        """Create a token for update email address."""
        serializer = TokenUpdateEmailSerializers(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We have sent an email for you to update email address.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_email(self, request, *args, **kwargs):
        """Update user's email address."""
        serializer = UpdateEmailSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Updated email address'}
        return Response(data, status=status.HTTP_200_OK)
