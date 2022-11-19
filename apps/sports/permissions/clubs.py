"""Clubs permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission
from apps.users.models import User


class IsTrainer(BasePermission):
    """Allow access only to trainers."""

    def has_permission(self, request, view):
        """Check user's role."""
        return request.user.role == User.Roles.trainer


class IsClubOwner(BasePermission):
    """Allow access only to owner the club."""

    def has_permission(self, request, view):
        obj = view.club if hasattr(view, 'club') else view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Check requesting user is owner of the club."""
        return obj.trainer == request.user
