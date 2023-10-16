from datetime import datetime

from app.middlewares.authtoken import WebSocketAuthToken
from app.schemas.chat import ReadMessageSchema
from app.templates import club_chat
from app.utils.websockets import validate_club_member
from fastapi import Depends, FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from settings import mongo_client
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=WebSocketAuthToken())


@app.get('/chat')
async def chat():
    """Render chat template."""
    return HTMLResponse(club_chat)


@app.websocket('/chat/clubs/{slug}/ws')
async def club_messages(
    websocket: WebSocket,
    slug: str,
    deps: tuple = Depends(validate_club_member)
):
    """Send or get messages to/of a club."""
    user, _ = deps
    await websocket.accept()
    messages = mongo_client.local.messages.find({'room': slug})
    data = [
        dict(
            ReadMessageSchema(**{**message, '_id': str(message['_id'])})
        ) for message in messages
    ]
    await websocket.send_json(data)
    while True:
        now = datetime.now()
        data = {
            'text': await websocket.receive_text(),
            'sender': user.username,
            'date': now.strftime('%d-%m-%Y, %H:%M'),
            'room': slug
        }
        data['_id'] = str(mongo_client.local.messages.insert_one(data).inserted_id)
        await websocket.send_json([data])
