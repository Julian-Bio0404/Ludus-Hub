"""Tournament views."""

from apps.sports.models import Round, Tournament
from apps.sports.permissions import HasCompetitors, IsTournamentCreator
from apps.sports.serializers import (AddCompetitorSerializer,
                                     CompetitorModelSerializer,
                                     CreateDrawSerializer,
                                     CreateTournamentSerializer,
                                     DrawModelSerializer,
                                     RoundModelSerializer,
                                     TournamentModelSerializer)
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


class RoundViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    Round viewset.
    Handle list and retrieve rounds.
    """

    serializer_class = RoundModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        return [IsAuthenticated()]

    def get_queryset(self):
        return Round.objects.filter(draw__tournament=self.tournament)

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, id=kwargs['id'])
        return super(RoundViewSet, self).dispatch(request, *args, **kwargs)
