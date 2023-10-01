"""Tournament permissions."""

from rest_framework.permissions import BasePermission


class HasCompetitors(BasePermission):
    """Allow actions only on tournaments without competitors."""

    message = 'The tournament already has competitors!'

    def has_object_permission(self, request, view, obj):
        """Check that tournament user has not competitors."""
        return not obj.competitor_set.exists()


class IsTournamentCreator(BasePermission):
    """Allow access only to tournament creator."""

    def has_permission(self, request, view):
        if hasattr(view, 'tournament'):
            return request.user == view.tournament.creator
        return True

    def has_object_permission(self, request, view, obj):
        """Check that requesting user is the tournament creator."""
        tournament = obj.tournament if hasattr(view, 'tournament') else obj
        return request.user == tournament.creator


class IsCreatorOrInvited(BasePermission):
    """Allow access only to invitation creator."""

    def has_object_permission(self, request, view, obj):
        """Check that requesting user is the tournament creator or invited."""
        return request.user in [obj.sent_by, obj.invited]


class IsInvited(BasePermission):
    """Allow access only to referee invited."""

    def has_object_permission(self, request, view, obj):
        """Check that requesting user is invited."""
        return request.user == obj.invited
