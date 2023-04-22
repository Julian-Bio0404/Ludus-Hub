"""Plan serializers."""

from apps.payments.models import Plan
from rest_framework import serializers


class PlanModelSerializer(serializers.ModelSerializer):
    """Plan model serializer."""

    amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_currency(self, obj):
        return obj.price.currency.upper()

    def get_amount(self, obj):
        return obj.price.amount

    class Meta:
        """Meta options."""
        model = Plan
        fields = [
            'id', 'stripe_id',
            'name', 'amount',
            'currency', 'interval',
            'description'
        ]
