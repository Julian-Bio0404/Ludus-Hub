from __future__ import absolute_import, unicode_literals

from apps.payments.models import Plan
from apps.utils.payments import StripeClient
from taskapp.celery import app


@app.task(bind=True)
def create_stripe_plan(self, id) -> bool:
    """Create a stripe plan."""
    plan = Plan.objects.get(id=id)
    client = StripeClient()
    data = {
        'interval': plan.interval,
        'amount_decimal': plan.price.amount * 100,
        'currency': plan.price.currency,
        'product': {
            'name': plan.name
        }
    }
    if plan.description:
        data['nickname'] = plan.description
    response = client.plan.create(**data)
    plan.stripe_id = response['id']
    plan.product_id = response['product']
    plan.save()
    return True


@app.task(bind=True)
def update_stripe_plan(self, id) -> bool:
    """Update a stripe plan."""
    client = StripeClient()
    plan = Plan.objects.get(id=id)
    client.plan.update(plan.stripe_id, nickname=plan.description)
    return True


@app.task(bind=True)
def delete_stripe_plan(self, id) -> bool:
    """Delete a stripe plan."""
    client = StripeClient()
    response = client.plan.delete(id)
    return response['deleted']
