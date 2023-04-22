"""Subscription permissions."""

from rest_framework.permissions import BasePermission


class HasNoSubscription(BasePermission):
    """Allow access only to users that do not have subscription."""

    def has_permission(self, request, view):
        """Check user subscription."""
        subscription = request.user._subscription
        return bool(not subscription or not subscription.active)
