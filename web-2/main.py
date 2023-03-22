from datetime import datetime

from app.middlewares.authtoken import WebSocketAuthToken
from app.queries import clubs
from app.schemas.chat import ReadMessageSchema
from fastapi import FastAPI, WebSocket, WebSocketException, status
from fastapi.responses import HTMLResponse
from settings import get_db, mongo_client
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=WebSocketAuthToken())


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form>
            <label>Club Slug: <input type="text" id="clubSlug" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button type="button" onclick="connect()">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button type="button" onclick="sendMessage()">Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = null;
            function connect() {
                var clubSlug = document.getElementById("clubSlug")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8001/chat/clubs/" + clubSlug.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
            }
            function sendMessage() {
                var input = document.getElementById("messageText")
                if (ws != null && input.value != "") {
                    ws.send(input.value)
                    input.value = ''
                }
            }
        </script>
    </body>
</html>
"""


@app.get('/chat')
async def chat():
    """Render chat template."""
    return HTMLResponse(html)


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
