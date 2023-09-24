"""Tournament views."""

from apps.sports.models import Tournament
from apps.sports.permissions import (HasCompetitors, IsCreatorOrInvited,
                                     IsInvited, IsTournamentCreator)
from apps.sports.serializers import (AddAdminSerializer,
                                     AddCompetitorSerializer,
                                     CompetitorModelSerializer,
                                     CreateDrawSerializer,
                                     CreateRefereeInvitationSerializer,
                                     CreateTournamentSerializer,
                                     DrawModelSerializer,
                                     RefereeInvitationModelSerializer,
                                     TournamentModelSerializer)
from apps.users.serializers import UserModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TournamentViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Tournament viewset.
    Handle all crud actions for Tournaments.
    """

    queryset = Tournament.objects.all()
    serializer_class = TournamentModelSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('slug', 'date')
    ordering = ('date',)
    filterset_fields = ('slug', 'type', 'sport__slug')

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions = [
                IsAuthenticated,
                IsTournamentCreator,
                HasCompetitors
            ]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateTournamentSerializer(
            data=data, context={'creator': self.request.user})
        serializer.is_valid(raise_exception=True)
        tournament = serializer.save()
        data = TournamentModelSerializer(tournament).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def inscriptions(self, request, *args, **kwargs):
        data = request.data
        serializer = AddCompetitorSerializer(
            data=data, context={'tournament': self.get_object()})
        serializer.is_valid(raise_exception=True)
        competitor = serializer.save()
        data = CompetitorModelSerializer(competitor).data
        return Response(data=data, status=status.HTTP_201_CREATED)


class CompetitorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Competitor viewset.
    List or delete competitors.
    """

    serializer_class = CompetitorModelSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('created', 'athlete__username', 'team__slug')
    ordering = ('created',)
    filterset_fields = ('athlete__username', 'team__slug', 'category__id')

    def get_permissions(self):
        """Assign permissions based on action."""
        return [IsAuthenticated()]

    def get_queryset(self):
        return self.tournament.competitor_set.all()

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, id=kwargs['id'])
        return super(CompetitorViewSet, self).dispatch(request, *args, **kwargs)


class DrawViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Draw viewset.
    Handle all crud actions for draws of a tournament.
    """

    serializer_class = DrawModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        return [IsAuthenticated()]

    def get_queryset(self):
        return self.tournament.draw_set.all()

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, id=kwargs['id'])
        return super(DrawViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateDrawSerializer(
            data=data, context={'tournament': self.tournament})
        serializer.is_valid(raise_exception=True)
        draw = serializer.save()
        data = DrawModelSerializer(draw).data
        return Response(data=data, status=status.HTTP_201_CREATED)


class AdministratorViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    Administrator viewset.
    Handle list, add and remove tournament administrators.
    """

    serializer_class = UserModelSerializer

    def get_queryset(self):
        return self.tournament.administrators.all()

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, id=kwargs['id'])
        return super(AdministratorViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Add or remove admins to a tournament."""
        data = request.data
        serializer = AddAdminSerializer(
            data=data, context={'tournament': self.tournament})
        serializer.is_valid(raise_exception=True)
        tournament = serializer.save()
        administrators = tournament.administrators.all()
        data = UserModelSerializer(administrators, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class RefereeInvitationViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Referee viewset.
    Handle list, update, and remove referee invitations.
    """

    serializer_class = RefereeInvitationModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsCreatorOrInvited)
        elif self.action in ['update', 'partial_update']:
            permissions.append(IsInvited)
        return [p() for p in permissions]

    def get_queryset(self):
        return self.tournament.referee_invitations.all()

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, id=kwargs['id'])
        return super(RefereeInvitationViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create referee invitations."""
        data = request.data
        creator = request.user
        serializer = CreateRefereeInvitationSerializer(
            data=data,
            context={'tournament': self.tournament, 'creator': creator})
        serializer.is_valid(raise_exception=True)
        invitations = serializer.save()
        data = RefereeInvitationModelSerializer(invitations, many=True).data
        return Response(data=data, status=status.HTTP_201_CREATED)
