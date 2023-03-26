from __future__ import absolute_import, unicode_literals

from apps.payments.models import Plan
from apps.utils.payments import StripeClient
from taskapp.celery import app


@app.task(bind=True)
def create_stripe_plan(self, id):
    """Create a stripe plan."""
    plan = Plan.objects.get(id=id)
    client = StripeClient()
    data = {
        'name': plan.name,
        'interval': plan.interval,
        'description': plan.description,
        'amount': plan.price.amount,
        'product': {
            'name': plan.name
        }
    }
    client.plan.create(**data)
    return True
