"""Plan views."""

from rest_framework import mixins, viewsets
from apps.payments.models import Plan
from apps.payments.serializers import PlanModelSerializer


class PlanViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Plan viewset.
    Handle retrieve and list plans.
    """

    queryset = Plan.objects.all()
    serializer_class = PlanModelSerializer
