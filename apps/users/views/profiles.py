"""Profile views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsProfileOwner

# Models
from apps.users.models import Profile

# Serializers
from apps.users.serializers import ProfileModelSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Profile viewset.
    Handle update, retrieve and list profiles
    """

    queryset = Profile.objects.filter(
        user__verified=True).select_related('user')
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsProfileOwner)
        return [p() for p in permissions]
