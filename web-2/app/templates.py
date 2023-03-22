club_chat = """
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
