document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on("message", data => {
		console.log(data)
		io.emit("message",data)
    });
});
