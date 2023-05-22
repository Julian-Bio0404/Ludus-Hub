"""Clubs views."""

from apps.sports.models import Club
from apps.sports.permissions import IsClubOwner, IsTrainer
from apps.sports.serializers import ClubModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated


class ClubViewSet(viewsets.ModelViewSet):
    """
    Club Viewset.
    Handles create, detail, update and destroy club.
    """

    queryset = Club.objects.all().select_related('trainer')
    serializer_class = ClubModelSerializer
    lookup_field = 'slug'
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('slug',)
    filterset_fields = ('city', 'sport__slug')

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['create']:
            permissions.append(IsTrainer)
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsClubOwner)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add trainer to serializer context."""
        context = super(ClubViewSet, self).get_serializer_context()
        context['trainer'] = self.request.user
        return context
