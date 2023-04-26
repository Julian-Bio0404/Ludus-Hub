"""Sport views."""

from apps.sports.models import Sport
from apps.sports.serializers import SportModelSerializer
from rest_framework import mixins, viewsets


class SportViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    Sport viewset.
    Handle retrieve and list profiles
    """

    queryset = Sport.objects.all()
    serializer_class = SportModelSerializer
