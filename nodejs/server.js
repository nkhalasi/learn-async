var net = require('net');
var HOST = '0.0.0.0';
var PORT = 2992;

var clients = []
var server = net.createServer();
server.listen(PORT, HOST);

server.on('connection', function(sock) {
    sock.setEncoding('utf8');
    sock.name = sock.remoteAddress + ':' + sock.remotePort;
    clients.push(sock);

    console.log('CONNECTED: ' + sock.remoteAddress + ':' + sock.remotePort);
    //sock.write('HELLO\n'); //send a hello to let the client know they are connected

    sock.on('data', socket_data_handler);
    sock.on('close', socket_close_handler);

    function socket_data_handler(data) {
        console.log('Received ' + data);
        if (data != 'WORLD') {
            console.log('Expected WORLD, received ' + data);
            sock.write('BYE');
        } else {
            sock.write('READY\n');
        }

        if (data === 'BYE\n') {
            sock.end();
        }
    }

    function socket_close_handler(data) {
        clients.splice(clients.indexOf(sock), 1);
        console.log('CLOSED: ' + sock.remoteAddress + ':' + sock.remotePort);
    }
});


console.log('Server listening on ' + HOST + ':' + PORT);
