from datetime import datetime

from app.middlewares.authtoken import WebSocketAuthToken
from app.schemas.chat import ReadMessageSchema
from app.templates import club_chat, user_chat
from app.utils.websockets import validate_club_member, validate_users
from fastapi import Depends, FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from settings import mongo_client
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=WebSocketAuthToken())


@app.get('/club-chat')
async def render_club_chat():
    """Render club chat template."""
    return HTMLResponse(club_chat)


@app.get('/user-chat')
async def render_user_chat():
    """Render user chat template."""
    return HTMLResponse(user_chat)


@app.websocket('/chat/clubs/{id}/ws')
async def club_messages(
    websocket: WebSocket,
    id: str,
    deps: tuple = Depends(validate_club_member)
):
    """Send or get messages user <-> club."""
    user, _ = deps
    messages = mongo_client.local.messages.find({'channel': id})
    data = [
        dict(
            ReadMessageSchema(**{**message, '_id': str(message['_id'])})
        ) for message in messages
    ]
    await websocket.accept()
    await websocket.send_json(data)
    while True:
        now = datetime.now()
        data = {
            'text': await websocket.receive_text(),
            'sender': str(user.id),
            'date': now.strftime('%d-%m-%Y, %H:%M'),
            'channel': id
        }
        data['_id'] = str(mongo_client.local.messages.insert_one(data).inserted_id)
        await websocket.send_json([data])


@app.websocket('/chat/users/{id}/ws')
async def user_messages(
    websocket: WebSocket,
    id: str,
    deps: tuple = Depends(validate_users)
):
    """Send or get messages user <-> user."""
    sender, receiver = deps
    messages = mongo_client.local.messages.find({
        '$and': [
            {'sender': {'$in': [str(sender.id), str(receiver.id)]}},
            {'receiver': {'$in': [str(sender.id), str(receiver.id)]}}
        ]
    })

    data = [
        dict(
            ReadMessageSchema(**{**message, '_id': str(message['_id'])})
        ) for message in messages
    ]
    await websocket.accept()
    await websocket.send_json(data)
    while True:
        now = datetime.now()
        data = {
            'text': await websocket.receive_text(),
            'sender': str(sender.id),
            'receiver': str(receiver.id),
            'date': now.strftime('%d-%m-%Y, %H:%M')
        }
        data['_id'] = str(mongo_client.local.messages.insert_one(data).inserted_id)
        await websocket.send_json([data])
