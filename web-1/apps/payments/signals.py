"""Payment signals."""

from apps.payments.models import Plan
from django.db.models.signals import post_save
from django.dispatch import receiver
from taskapp.tasks import create_stripe_plan


@receiver(post_save, sender=Plan)
def plan_post_save(sender, instance, created, **kwargs):
    """Set of actions executed after a plan is created."""
    if created:
        create_stripe_plan.delay(id=instance.id)
