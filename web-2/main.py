from datetime import datetime

from app.middlewares.authtoken import AuthTokenBackend
from app.queries import clubs
from app.schemas.chat import ReadMessageSchema
from fastapi import Request
from settings import get_db, mongo_client
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route


@requires('authenticated')
async def send_message(request: Request):
    """Send a message."""
    user = request.user
    club_slug = request.path_params['slug']
    db = get_db()
    club = clubs.get_club(next(db), slug=club_slug)
    if not club:
        content = {'detail': 'Club does not exist'}
        return JSONResponse(content=content, status_code=403)

    members = [i.user.username for i in club.members]
    if user.username not in members:
        content = {'detail': 'Do you not have permission for this action'}
        return JSONResponse(content=content, status_code=404)

    now = datetime.now()
    data = await request.json()
    data['sender'] = user.username
    data['date'] = now.strftime('%d-%m-%Y, %H:%M')
    data['room'] = club_slug
    mongo_client.local.messages.insert_one(data)
    content = {'message': 'Message sent!'}
    return JSONResponse(content=content, status_code=201)


@requires('authenticated')
def get_messages(request: Request):
    """Get all messages."""
    user = request.user
    club_slug = request.path_params['slug']
    db = get_db()
    club = clubs.get_club(next(db), slug=club_slug)
    if not club:
        content = {'detail': 'Club does not exist'}
        return JSONResponse(content=content, status_code=404)

    members = [i.user.username for i in club.members]
    if user.username not in members:
        content = {'detail': 'Do you not have permission for this action'}
        return JSONResponse(content=content, status_code=403)

    messages = mongo_client.local.messages.find({'room': club_slug})
    data = [dict(ReadMessageSchema(**message)) for message in messages]
    return JSONResponse(content=data, status_code=200)


middleware = [
    Middleware(AuthenticationMiddleware, backend=AuthTokenBackend())
]

routes = [
    Route('/club/{slug:str}/send-message', endpoint=send_message, methods=['POST']),
    Route('/club/{slug:str}/messages', endpoint=get_messages)
]

app = Starlette(routes=routes, middleware=middleware)
