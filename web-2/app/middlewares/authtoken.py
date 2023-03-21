from app.models.users import Token
from fastapi import HTTPException, WebSocketException, status
from settings import get_db
from sqlalchemy.orm import Session
from starlette.authentication import AuthCredentials, AuthenticationBackend


def verify_token(key: str, db: Session) -> Token:
    """Verify token."""
    key = key.replace('Token ', '')
    token = db.query(Token).filter(Token.key == key).first()
    return token


class WebSocketAuthToken(AuthenticationBackend):
    """Custom auth token backend for websocket."""

    async def authenticate(self, conn):
        """Check the token key."""
        key = conn.query_params.get('token')
        if not key:
            return

        try:
            db = get_db()
            token = verify_token(key, next(db))
            if not token:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        except HTTPException as e:
            raise e
        return AuthCredentials(['authenticated']), token.user
