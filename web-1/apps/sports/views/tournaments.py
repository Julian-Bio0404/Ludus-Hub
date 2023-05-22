"""Tournament views."""

from apps.sports.models import Tournament
from apps.sports.serializers import (CreateTournamentSerializer,
                                     TournamentModelSerializer)
from rest_framework import mixins, status, viewsets
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
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateTournamentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        tournament = serializer.save()
        data = TournamentModelSerializer(tournament).data
        return Response(data=data, status=status.HTTP_201_CREATED)
