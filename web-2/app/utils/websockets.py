import logging

from app.queries import clubs
from fastapi import WebSocket, WebSocketException, status
from settings import get_db


async def validate_club_member(websocket: WebSocket, slug: str):
    """Check that the user belongs to the club."""
    user = websocket.scope.get('user')
    if not user:
        exception = WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='You must provide the authentication credentials')
        logging.error(exception.__repr__())
        raise exception

    db = get_db()
    club = clubs.get_club(next(db), slug=slug)
    if not club:
        exception = WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='Club does not exist')
        logging.error(exception.__repr__())
        raise exception

    members = [i.user.username for i in club.members]
    if user.username not in members:
        exception = WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='Do you not have permission for this action')
        logging.error(exception.__repr__())
        raise exception

    return user, club
