"""Profile views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Models
from apps.users.models import User

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsProfileOwner

# Serializers
from apps.users.serializers import UserModelSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Profile viewset.
    Handle update, retrieve and list profiles
    """

    queryset = User.objects.filter(verified=True).select_related('profile')
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsProfileOwner)
        return [p() for p in permissions]
