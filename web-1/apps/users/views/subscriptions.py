"""Subscription views."""

from apps.users.serializers import SubscriptionModelSerializer
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated


class SubscriptionViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    Subscription viewset.
    Handle create, retrieve or cancellation of subscriptions.
    """

    serializer_class = SubscriptionModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_queryset(self):
        return self.request.user.subscription
