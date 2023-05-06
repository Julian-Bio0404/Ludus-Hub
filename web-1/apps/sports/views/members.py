"""Members views."""

from datetime import date

from apps.sports.models import Assistance, Club, Invitation, Member, Team
from apps.sports.permissions import (IsClubAdmin, IsInvited,
                                     IsSelfMemberOrClubOwner)
from apps.sports.serializers import (AssistanceModelSerializer,
                                     CreateAssistanceSerializer,
                                     CreateInvitationSerializer,
                                     CreateTeamSerializer,
                                     InvitationModelSerializer,
                                     MemberModelSerializer,
                                     TeamModelSerializer)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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

    @action(detail=True)
    def assistances(self, request, *args, **kwargs):
        member = self.get_object().user
        dates = Assistance.objects.filter(
            club=self.club, user=member).values_list('created', flat=True)
        dates = [date.strftime('%d-%m-%Y, %H:%M:%S') for date in dates]
        data = {'assistances': dates}
        return Response(data=data, status=status.HTTP_200_OK)


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

    serializer_class = AssistanceModelSerializer

    def get_queryset(self):
        today = date.today()
        return Assistance.objects.filter(club=self.club, created__gte=today)

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


class TeamViewset(viewsets.ModelViewSet):
    """
    Team view set.
    Create, retrieve, update, delete or
    list the team of a club.
    """

    serializer_class = TeamModelSerializer
    serializer_class = TeamModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action != 'list':
            permissions.append(IsClubAdmin)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.club = get_object_or_404(Club, slug=kwargs['slug'])
        return super(TeamViewset, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return club teams."""
        return Team.objects.filter(club=self.club)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateTeamSerializer(data=data, context={'club': self.club})
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        data = TeamModelSerializer(invitation).data
        return Response(data=data, status=status.HTTP_201_CREATED)
