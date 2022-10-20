"""Users views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

# Serializers
from apps.users.serializers import (AccountVerificationSerializer,
                                    UpdatePasswordSerializer,
                                    UserLoginSerializer, UserModelSerializer,
                                    UserSignUpSerializer)


class UserViewSet(viewsets.GenericViewSet):
    """
    User view set.
    Handle signup, login, account
    verification and update password.
    """

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['update_psswd']:
            permissions = [IsAuthenticated]
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
