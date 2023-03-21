from datetime import datetime

from app.middlewares.authtoken import WebSocketAuthToken
from app.queries import clubs
from app.schemas.chat import ReadMessageSchema
from fastapi import FastAPI, Request, WebSocket, WebSocketException
from fastapi.responses import HTMLResponse
from settings import get_db, mongo_client
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=WebSocketAuthToken())


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
    data = [dict(ReadMessageSchema(**{**message, '_id': str(message['_id'])})) for message in messages]
    return JSONResponse(content=data, status_code=200)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Club Slug: <input type="text" id="clubSlug" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var clubSlug = document.getElementById("clubSlug")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8001/clubs/" + clubSlug.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get('/')
async def get():
    return HTMLResponse(html)


@app.websocket('/clubs/{slug}/ws')
async def websocket_endpoint(websocket: WebSocket, slug: str):
    user = websocket.scope.get('user')
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}, for club: {slug}")
