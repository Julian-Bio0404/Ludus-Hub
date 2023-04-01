from __future__ import absolute_import, unicode_literals

from apps.payments.models import Plan
from apps.utils.payments import StripeClient
from taskapp.celery import app


@app.task(bind=True)
def create_stripe_plan(self, id) -> bool:
    """Create a stripe plan."""
    plan = Plan.objects.get(id=id)
    client = StripeClient()
    amount, decimals = plan.price.dissociate_amount()
    data = {
        'interval': plan.interval,
        'amount': amount,
        'currency': plan.price.currency,
        'product': {
            'name': plan.name
        }
    }
    response = client.plan.create(**data)
    plan.stripe_id = response['id']
    plan.save()
    return True


@app.task(bind=True)
def delete_stripe_plan(self, id) -> bool:
    """Delete a stripe plan."""
    client = StripeClient()
    response = client.plan.delete(id)
    return response['deleted']
