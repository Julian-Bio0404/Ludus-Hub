"""Clubs members permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsSelfMemberOrClubOwner(BasePermission):
    """Allow access only to club trainer or member owner of the obj."""

    def has_object_permission(self, request, view, obj):
        """
        Check that requesting user is club trainer or
        owner of the obj.
        """
        if hasattr(obj, 'user'):
            return request.user in (view.club.trainer, obj.user)
        elif hasattr(obj, 'invited'):
            return request.user in (view.club.trainer, obj.invited)
        return False


class IsClubAdmin(BasePermission):
    """Allow access only to club trainer or club admin."""

    def has_permission(self, request, view):
        """Check that requesting user is club trainer."""
        return request.user == view.club.trainer


class IsInvited(BasePermission):
    """Allow access only to invited user."""

    def has_object_permission(self, request, view, obj):
        """Check that requesting user is invited user."""
        return request.user == obj.invited
