import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]
port_number = sys.argv[2]
server_address = (server_name, port_numbers)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'client connected:', client_address)
        while True:
            data = connection.recv(16)
            print (sys.stderr, 'received "%s"' % data)
            if data == 'end\r\n':
                break
            if data == 'disconnect\r\n':
                break
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()
        if data == 'end\r\n':
            sys.exit()