import stripe
from django.conf import settings


class StripeProduct:
    """Stripe Product object."""

    def create(self, **kwargs) -> stripe.Product:
        product = stripe.Product.create(**kwargs)
        return product

    def delete(self, id: str) -> stripe.Product:
        response = stripe.Product.delete(id)
        return response


class StripePlan:
    """Stripe Plan object."""

    def create(self, **kwargs) -> stripe.Plan:
        plan = stripe.Plan.create(**kwargs)
        return plan

    def delete(self, id: str) -> stripe.Plan:
        response = stripe.Plan.delete(id)
        return response


class StripeClient:
    """Stripe client."""

    product = StripeProduct()
    plan = StripePlan()

    def __init__(self) -> None:
        self.api_key = settings.STRIPE_API_KEY
        stripe.api_key = self.api_key
