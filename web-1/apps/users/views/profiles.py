"""Profile views."""

from apps.users.models import User
from apps.users.permissions import IsProfileOwner
from apps.users.serializers import UserModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated


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
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('username',)
    filterset_fields = ('username', 'role')

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsProfileOwner)
        return [p() for p in permissions]
