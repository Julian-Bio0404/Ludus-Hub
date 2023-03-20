from app.models.users import Token
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from settings import get_db
from sqlalchemy.orm import Session
from starlette.authentication import AuthCredentials, AuthenticationBackend


def verify_token(key: str, db: Session) -> Token:
    """Verify token."""
    key = key.replace('Token ', '')
    token = db.query(Token).filter(Token.key == key).first()
    return token


class AuthTokenBackend(AuthenticationBackend):
    """Custom auth token backend."""

    async def authenticate(self, conn):
        """Check the token key."""
        auth = conn.headers.get('authorization')
        if not auth:
            return

        try:
            scheme, key = auth.split()
            if scheme.lower() != 'token':
                return
            db = get_db()
            token = verify_token(key, next(db))
            if not token:
                return JSONResponse(content={'detail': 'Invalid token.'}, status_code=403)
        except HTTPException as e:
            return e
        return AuthCredentials(['authenticated']), token.user
