"""Members views."""

# Django REST framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.sports.permissions import IsClubAdmin, IsSelfMemberOrClubOwner, IsInvited

# Models
from apps.sports.models import Club, Member, Invitation

# Serializers
from apps.sports.serializers import (CreateInvitationSerializer,
                                     InvitationModelSerializer,
                                     MemberModelSerializer)


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
        self.club = get_object_or_404(Club, slug=kwargs['slug'])
        return super(MemberViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return club members."""
        return Member.objects.filter(club=self.club).select_related('user')


class InvitationViewSet(viewsets.ModelViewSet):
    """
    Invitation view set.
    Create, retrieve, update and delete club invitations.
    """

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['create', 'list']:
            permissions.append(IsClubAdmin)
        elif self.action in ['destroy', 'retrieve']:
            permissions.append(IsSelfMemberOrClubOwner)
        elif self.action in ['update', 'partial_update']:
            permissions.append(IsInvited)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.club = get_object_or_404(Club, slug=kwargs['slug'])
        return super(InvitationViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Invitation.objects.filter(club=self.club)

    def get_serializer_class(self):
        """Return a serializer based on action."""
        if self.action == 'create':
            return CreateInvitationSerializer
        return InvitationModelSerializer

    def get_serializer_context(self):
        """Add admin club and club to serializer context."""
        context = super(InvitationViewSet, self).get_serializer_context()
        context['sent_by'] = self.request.user
        context['club'] = self.club
        return context
