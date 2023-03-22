club_chat = html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <style>
            .message-container {
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid black;
                background-color: #f0f0f0;
            }
            .sender {
                font-weight: bold;
                margin-right: 5px;
            }
            .date {
                font-size: 12px;
                color: gray;
            }
            .text {
                margin-top: 5px;
            }
        </style>
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
        <div id="message-container">
        </div>
        <script>
        var ws = null;
            function connect(event) {
                var clubSlug = document.getElementById("clubSlug")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8001/chat/clubs/" + clubSlug.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messageContainer = document.getElementById('message-container');
                    var messages = JSON.parse(event.data);
                    messages.forEach(function(message) {
                        var div = document.createElement('div');
                        div.className = 'message-container';
                        var sender = document.createElement('span');
                        sender.className = 'sender';
                        sender.appendChild(document.createTextNode(message.sender));
                        var text = document.createElement('p');
                        text.className = 'text';
                        text.appendChild(document.createTextNode(message.text));
                        var date = document.createElement('span');
                        date.className = 'date';
                        date.appendChild(document.createTextNode(message.date));
                        div.appendChild(sender);
                        div.appendChild(text);
                        div.appendChild(date);
                        messageContainer.appendChild(div);
                    });
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
