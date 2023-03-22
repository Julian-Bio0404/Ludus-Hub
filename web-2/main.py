from datetime import datetime

from app.middlewares.authtoken import WebSocketAuthToken
from app.queries import clubs
from app.schemas.chat import ReadMessageSchema
from app.templates import club_chat
from fastapi import FastAPI, WebSocket, WebSocketException, status
from fastapi.responses import HTMLResponse
from settings import get_db, mongo_client
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=WebSocketAuthToken())


@app.get('/chat')
async def chat():
    """Render chat template."""
    return HTMLResponse(club_chat)


@app.websocket('/chat/clubs/{slug}/ws')
async def club_messages(websocket: WebSocket, slug: str):
    """Send or get messages to/of a club."""
    user = websocket.scope.get('user')
    if not user:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='You must provide the authentication credentials')

    db = get_db()
    club = clubs.get_club(next(db), slug=slug)
    if not club:
        raise WebSocketException(
            code=status.WS_1014_BAD_GATEWAY,
            reason='Club does not exist')

    members = [i.user.username for i in club.members]
    if user.username not in members:
        raise WebSocketException(
            code=status.WS_1014_BAD_GATEWAY,
            reason='Do you not have permission for this action')

    await websocket.accept()
    messages = mongo_client.local.messages.find({'room': slug})
    data = [
        dict(
            ReadMessageSchema(**{**message, '_id': str(message['_id'])})
        ) for message in messages
    ]
    await websocket.send_json(data)
    while True:
        data = {}
        now = datetime.now()
        data['text'] = await websocket.receive_text()
        data['sender'] = user.username
        data['date'] = now.strftime('%d-%m-%Y, %H:%M')
        data['room'] = slug
        id = mongo_client.local.messages.insert_one(data).inserted_id
        messages = mongo_client.local.messages.find({'_id': id})
        data = [
            dict(
                ReadMessageSchema(**{**message, '_id': str(message['_id'])})
            ) for message in messages
        ]
        await websocket.send_json(data)
