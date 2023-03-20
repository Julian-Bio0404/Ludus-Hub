from app.models.users import Token
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from settings import get_db
from sqlalchemy.orm import Session

app = FastAPI()


def verify_token(key: str, db: Session) -> Token:
    """Verify token."""
    key = key.replace('Token ', '')
    token = db.query(Token).filter(Token.key == key).first()
    return token


@app.middleware('http')
async def auth_middleware(request: Request, call_next):
    """Validate auth user."""
    key = request.headers.get('Authorization')
    if key:
        try:
            db = get_db()
            token = verify_token(key, next(db))
            if not token:
                return JSONResponse(content={'detail': 'Invalid token.'}, status_code=403)
        except HTTPException as e:
            return e
    else:
        return JSONResponse(content={'detail': 'Authentication credentials were not provided.'}, status_code=403)

    request.state.user = token.user
    response = await call_next(request)
    return response
