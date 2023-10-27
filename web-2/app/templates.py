club_chat = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #E5E5E5;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }

            h1 {
                text-align: center;
                margin-top: 20px;
                color: #4A90E2;
            }

            #top-form {
                background-color: #FFFFFF;
                padding: 20px;
                border-bottom: 2px solid #E5E5E5;
                display: flex;
                justify-content: flex-start;
                align-items: center;
            }

            #top-form label input {
                padding: 10px;
                margin-right: 10px;
                border-radius: 5px;
                border: 1px solid #E5E5E5;
            }

            #bottom-form {
                background-color: #FFFFFF;
                padding: 20px;
                border-top: 2px solid #E5E5E5;
                position: fixed;
                bottom: 0;
                width: 98%;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            #messageText {
                flex-grow: 1;
                margin-right: 10px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #E5E5E5;
            }

            button {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                cursor: pointer;
            }

            button:hover {
                background-color: #357ABD;
            }

            .message-container {
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #E5E5E5;
                background-color: #FFFFFF;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .sender {
                font-weight: bold;
                display: block;
            }

            .date {
                font-size: 12px;
                color: gray;
            }

            .text {
                margin-top: 5px;
                display: flex;
                justify-content: space-between;
                width: 100%;
            }

        </style>
    </head>
    <body>
        <h1>Club Chat</h1>
        <form id="top-form" action="" onsubmit="event.preventDefault();">
            <label>Club ID: <input type="text" id="clubID" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
        </form>
        <div id="message-container" style="padding: 20px; flex: 1; overflow-y: auto;">
        </div>
        <form id="bottom-form" action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="Type a message"/>
            <button>Send</button>
        </form>
        <script>
        var ws = null;
            function connect(event) {
                var clubID = document.getElementById("clubID")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8001/chat/clubs/" + clubID.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messageContainer = document.getElementById('message-container');
                    var messages = JSON.parse(event.data);
                    messages.forEach(function(message) {
                        var div = document.createElement('div');
                        div.className = 'message-container';
                        var sender = document.createElement('span');
                        sender.className = 'sender';
                        sender.appendChild(document.createTextNode(message.sender));
                        var textAndDate = document.createElement('div');
                        textAndDate.className = 'text';
                        var text = document.createElement('span');
                        text.appendChild(document.createTextNode(message.text));
                        var date = document.createElement('span');
                        date.className = 'date';
                        date.appendChild(document.createTextNode(message.date));
                        textAndDate.appendChild(text);
                        textAndDate.appendChild(date);
                        div.appendChild(sender);
                        div.appendChild(textAndDate);
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


user_chat = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #E5E5E5;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }

            h1 {
                text-align: center;
                margin-top: 20px;
                color: #4A90E2;
            }

            #top-form {
                background-color: #FFFFFF;
                padding: 20px;
                border-bottom: 2px solid #E5E5E5;
                display: flex;
                justify-content: flex-start;
                align-items: center;
            }

            #top-form label input {
                padding: 10px;
                margin-right: 10px;
                border-radius: 5px;
                border: 1px solid #E5E5E5;
            }

            #bottom-form {
                background-color: #FFFFFF;
                padding: 20px;
                border-top: 2px solid #E5E5E5;
                position: fixed;
                bottom: 0;
                width: 98%;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            #messageText {
                flex-grow: 1;
                margin-right: 10px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #E5E5E5;
            }

            button {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                cursor: pointer;
            }

            button:hover {
                background-color: #357ABD;
            }

            .message-container {
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #E5E5E5;
                background-color: #FFFFFF;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .sender {
                font-weight: bold;
                display: block;
            }

            .date {
                font-size: 12px;
                color: gray;
            }

            .text {
                margin-top: 5px;
                display: flex;
                justify-content: space-between;
                width: 100%;
            }

        </style>
    </head>
    <body>
        <h1>User Chat</h1>
        <form id="top-form" action="" onsubmit="event.preventDefault();">
            <label>User ID: <input type="text" id="userID" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
        </form>
        <div id="message-container" style="padding: 20px; flex: 1; overflow-y: auto;">
        </div>
        <form id="bottom-form" action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="Type a message"/>
            <button>Send</button>
        </form>
        <script>
        var ws = null;
            function connect(event) {
                var userID = document.getElementById("userID")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8001/chat/users/" + userID.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messageContainer = document.getElementById('message-container');
                    var messages = JSON.parse(event.data);
                    messages.forEach(function(message) {
                        var div = document.createElement('div');
                        div.className = 'message-container';
                        var sender = document.createElement('span');
                        sender.className = 'sender';
                        sender.appendChild(document.createTextNode(message.sender));
                        var textAndDate = document.createElement('div');
                        textAndDate.className = 'text';
                        var text = document.createElement('span');
                        text.appendChild(document.createTextNode(message.text));
                        var date = document.createElement('span');
                        date.className = 'date';
                        date.appendChild(document.createTextNode(message.date));
                        textAndDate.appendChild(text);
                        textAndDate.appendChild(date);
                        div.appendChild(sender);
                        div.appendChild(textAndDate);
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
