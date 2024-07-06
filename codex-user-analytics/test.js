const WebSocketClient = require('websocket').client;
const chatSocket = new WebSocketClient();

chatSocket.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

chatSocket.on('connect', function(connection) {
    console.log('WebSocket Client Connected');
    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });
    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log("Received: '" + message.utf8Data + "'");
        }
    });

    function sendNumber() {
        if (connection.connected) {
            const message = {
                'message': 'Hello, world!'
            };
            connection.sendUTF(JSON.stringify(message));
            setTimeout(sendNumber, 1000);
        }
    }
    sendNumber();
});

chatSocket.connect('ws://localhost:8000/ws/chat/');