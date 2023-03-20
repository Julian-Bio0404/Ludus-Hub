from app.middlewares.authtoken import AuthTokenBackend
from app.queries import clubs
from app.schemas.chat import (CreateMessageSchema, MessageSchema,
                              ReadMessageSchema)
from fastapi import Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from settings import get_db, mongo_client
from sqlalchemy.orm import Session
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route


@requires('authenticated')
def read_club(slug: str, request: Request, db: Session = Depends(get_db)):
    club = clubs.get_club(db, slug=slug)
    if not club:
        raise HTTPException(status_code=404, detail='Club does not exists')
    return club


@requires('authenticated')
def send_message(message: MessageSchema, request: Request):
    """Send a message."""
    data = jsonable_encoder(message)
    message = mongo_client.local.messages.insert_one(data)
    return message


@requires('authenticated')
def get_messages(request: Request):
    """Get all messages."""
    user = request.user
    messages = mongo_client.local.messages.find({'sender': user.username})
    data = [dict(ReadMessageSchema(**message)) for message in messages]
    return JSONResponse(content=data, status_code=200)


middleware = [
    Middleware(AuthenticationMiddleware, backend=AuthTokenBackend())
]

routes = [
    Route('/club/{slug}', endpoint=read_club),
    Route('/send-message', endpoint=send_message),
    Route('/messages', endpoint=get_messages)
]

app = Starlette(routes=routes, middleware=middleware)
