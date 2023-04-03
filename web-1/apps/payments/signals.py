"""Payment signals."""

from apps.payments.models import Plan
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from taskapp.tasks import create_stripe_plan, delete_stripe_plan, update_stripe_plan


@receiver(post_save, sender=Plan)
def plan_post_save(sender, instance, created, **kwargs):
    """Set of actions executed after a plan is created."""
    if created:
        post_save.disconnect(plan_post_save, sender=sender)
        create_stripe_plan.delay(id=instance.id)
        post_save.connect(plan_post_save, sender=sender)
    else:
        if instance.description:
            update_stripe_plan.delay(id=instance.id)


@receiver(post_delete, sender=Plan)
def plan_post_delete(sender, instance, **kwargs):
    """Set of actions executed after a plan is deleted."""
    delete_stripe_plan.delay(id=instance.stripe_id)
