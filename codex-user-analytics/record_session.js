
    const socket = new WebSocket('ws://localhost:8000/ws/recordings/');

    socket.onopen = function(event) {
        rrweb.record({
            emit(event) {
                socket.send(JSON.stringify(event));
            }
        });
    };

    socket.onmessage = function(event) {
        console.log('Message from server:', event.data);
    };

    socket.onclose = function(event) {
        console.log('WebSocket is closed now.');
    };

    socket.onerror = function(error) {
        console.error('WebSocket Error:', error);
    };
