import stripe
from django.conf import settings


class StripeProduct:
    """Stripe Product object."""

    def create(self, **kwargs) -> stripe.Product:
        return stripe.Product.create(**kwargs)

    def delete(self, id: str) -> stripe.Product:
        return stripe.Product.delete(id)


class StripePlan:
    """Stripe Plan object."""

    def create(self, **kwargs) -> stripe.Plan:
        return stripe.Plan.create(**kwargs)

    def update(self, id: str, **kwargs) -> stripe.Plan:
        return stripe.Plan.modify(id, **kwargs)

    def delete(self, id: str) -> stripe.Plan:
        return stripe.Plan.delete(id)


class StripeCheckout:
    """Stripe Checkout object."""

    def create(self, **kwargs) -> stripe.checkout.Session:
        return stripe.checkout.Session.create(**kwargs)


class StripeClient:
    """Stripe client."""

    product = StripeProduct()
    plan = StripePlan()
    checkout = StripeCheckout()

    def __init__(self) -> None:
        self.api_key = settings.STRIPE_API_KEY
        stripe.api_key = self.api_key
