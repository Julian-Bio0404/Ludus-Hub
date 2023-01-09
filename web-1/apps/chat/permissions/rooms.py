"""Chat Permissions."""


class WebsocketBasePermission:
    """
    A base class from which all permission
    classes should inherit.
    """

    def has_permission(self, scope: dict) -> bool:
        """
        Return `True` if permission is granted,
        `False` otherwise.
        """
        return True


class IsWebSocketAuthenticated(WebsocketBasePermission):
    """Allow access only to user authenticated to websockets."""

    def has_permission(self, scope: dict) -> bool:
        user = scope.get('user')
        return bool(user and user.is_authenticated)
