"""Subscription serializers."""

from apps.users.models import Subscription
from rest_framework import serializers


class SubscriptionModelSerializer(serializers.ModelSerializer):
    """Subscription model serializer."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Subscription
        fields = [
            'user', 'plan', 'active',
            'created', 'updated'
        ]
