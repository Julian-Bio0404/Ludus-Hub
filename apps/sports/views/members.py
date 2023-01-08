"""Members views."""

from datetime import date

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.sports.permissions import (IsClubAdmin, IsInvited,
                                     IsSelfMemberOrClubOwner)

# Models
from apps.sports.models import Assistance, Club, Invitation, Member

# Serializers
from apps.sports.serializers import (AssistanceModelSerializer,
                                     CreateAssistanceSerializer,
                                     CreateInvitationSerializer,
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
    serializer_class = InvitationModelSerializer

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

    def get_serializer_context(self):
        """Add admin club and club to serializer context."""
        context = super(InvitationViewSet, self).get_serializer_context()
        context['sent_by'] = self.request.user
        context['club'] = self.club
        return context

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateInvitationSerializer(
            data=data, context={'sent_by': self.request.user, 'club': self.club})
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        data = InvitationModelSerializer(invitation).data
        return Response(data=data, status=status.HTTP_201_CREATED)


class AssistanceViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Asistance viewset.
    Handle bulk create and list asistances by club.
    """

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action == 'create':
            permissions.append(IsClubAdmin)
        elif self.action == 'list':
            permissions.append(IsSelfMemberOrClubOwner)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.club = get_object_or_404(Club, slug=kwargs['slug'])
        return super(AssistanceViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create assistances for each member of a club."""
        data = request.data
        serializer = CreateAssistanceSerializer(
            data=data, context={'club': self.club})
        serializer.is_valid(raise_exception=True)
        assistances = serializer.save()
        data = AssistanceModelSerializer(assistances, many=True).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """List assistance of a club on current day."""
        today = date.today()
        assistances = Assistance.objects.filter(created__gte=today)
        data = AssistanceModelSerializer(assistances, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
