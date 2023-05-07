"""Clubs views."""

# Django REST Framawork
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

# Filters
from rest_framework.filters import OrderingFilter, SearchFilter

# Permissions
from apps.sports.permissions import IsClubOwner, IsTrainer
from rest_framework.permissions import IsAuthenticated

# Models
from apps.sports.models import Club

# Serializers
from apps.sports.serializers import ClubModelSerializer


class ClubViewSet(viewsets.ModelViewSet):
    """
    Club Viewset.
    Handles create, detail, update and destroy club.
    """

    queryset = Club.objects.all().select_related('trainer')
    serializer_class = ClubModelSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug',)
    ordering_fields = ('slug',)
    ordering = ('slug',)
    filter_fields = ('city',)

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
