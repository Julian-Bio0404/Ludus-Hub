"""Tournament views."""

from apps.sports.models import Tournament
from apps.sports.permissions import HasCompetitors, IsTournamentCreator
from apps.sports.serializers import (AddCompetitorSerializer,
                                     CompetitorModelSerializer,
                                     CreateTournamentSerializer,
                                     TournamentModelSerializer)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
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

    def get_permissions(self):
        """Assign permissions based on action."""
        return [IsAuthenticated()]

    def get_queryset(self):
        return self.tournament.competitor_set.all()

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, id=kwargs['id'])
        return super(CompetitorViewSet, self).dispatch(request, *args, **kwargs)
