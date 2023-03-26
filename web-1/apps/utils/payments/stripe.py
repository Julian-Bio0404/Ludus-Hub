import stripe
from django.conf import settings


class StripeProduct:
    """Stripe Product object."""

    def create(self, **kwargs):
        product = stripe.Product.create(**kwargs)
        return product


class StripePlan:
    """Stripe Plan object."""

    def create(self, **kwargs):
        plan = stripe.Plan.create(**kwargs)
        return plan


class StripeClient:
    """Stripe client."""

    product = StripeProduct()
    plan = StripePlan()

    def __init__(self) -> None:
        self.api_key = settings.STRIPE_API_KEY
        stripe.api_key = self.api_key
