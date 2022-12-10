"""Members views."""

# Django REST framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.sports.permissions import IsClubAdmin, IsSelfMemberOrClubOwner

# Models
from apps.sports.models import Club, Member

# Serializers
from apps.sports.serializers import MemberModelSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    Member view set.
    Create, retrieve, expel or desactive
    a member and list the Club members.
    """

    serializer_class = MemberModelSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsClubAdmin)
        elif self.action in ['destroy']:
            permissions.append(IsSelfMemberOrClubOwner)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.club = get_object_or_404(Club, slugname=kwargs['slugname'])
        return super(MemberViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return club members."""
        return Member.objects.filter(club=self.club).select_related('user')
