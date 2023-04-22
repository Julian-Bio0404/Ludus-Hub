"""Subscription views."""

from apps.users.models import Subscription
from apps.users.permissions import HasNoSubscription
from apps.users.serializers import (CreateSubscriptionSerializer,
                                    SubscriptionModelSerializer)
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    Subscription viewset.
    Handle create, retrieve or cancellation of subscriptions.
    """

    serializer_class = SubscriptionModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['create']:
            permissions.append(HasNoSubscription)
        return [p() for p in permissions]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateSubscriptionSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        data = SubscriptionModelSerializer(subscription).data
        return Response(data, status=status.HTTP_201_CREATED)
