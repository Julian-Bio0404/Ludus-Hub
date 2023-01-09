"""Profile permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj) -> bool:
        """Check obj and user profile are the same."""
        return request.user == obj
