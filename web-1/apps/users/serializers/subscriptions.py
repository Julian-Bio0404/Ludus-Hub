"""Subscription serializers."""

from apps.users.models import Subscription
from rest_framework import serializers
from apps.payments.models import Card, Plan
from apps.utils.payments import StripeClient


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


class CreateSubscriptionSerializer(serializers.Serializer):
    """Handle the subscription creation."""

    plan_id = serializers.UUIDField()

    payment_method = serializers.DictField()

    def validate(self, data):
        """Verify the plan id and payment mehotd."""
        try:
            plan = Plan.objects.get(id=data['plan_id'])
        except Plan.DoesNotExist:
            raise serializers.ValidationError('Plan Does not exist.')

        user = self.context['user']
        client = StripeClient()

        if not user.customer_id:
            customer = client.customer.create(**data)
            user.customer_id = customer['id']
            user.save()
        else:
            customer = client.customer.get(id=user.customer_id)

        last4 = data['payment_method']['number'][-4:]
        card = Card.objects.filter(user=user, last4=last4).last()
        if not card:
            response = client.customer.create_source(
                user.customer_id, {'source': data['payment_method']['source']}
            )
            card = Card.objects.create(user=user, stripe_id=response['id'], last4=response['last4'])
        self.context['plan'] = plan
        self.context['card'] = card
        return data

    def create(self, data):
        user = self.context['user']
        plan = self.context['plan']
        card = self.context['card']

        subs_data = {
            'customer': user.customer_id,
            'items': [{'price': plan.stripe_id}],
            'currency': plan.price.currency,
            'default_source': card.stripe_id
        }
        client = StripeClient()
        client.subscription.create(**subs_data)
        subscription = Subscription.objects.update_or_create(
            user=user,
            defaults={
                'plan': plan,
                'active': True
            }
        )
        return subscription
