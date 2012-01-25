#!/usr/bin/python
"""
recho client, usage:

 python recho_client.py <host> <port>

Both host and port are optional, defaults: localhost 50000
host must be present if you want to provide port

Prompt user for each message to send
Repeat sending messages until user enters empty string
"""

import socket
import sys
import select

host = 'localhost'
port = 50003
size = 1024

nargs = len(sys.argv)
if nargs > 1:
    host = sys.argv[1]
if nargs > 2:
    port = int(sys.argv[2])

my_socket = socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM)
my_socket.connect((host,port))
print 'Connection accepted by (%s,%s)' % (host, port)
print 'Enter to quit'
sys.stdout.write('> ')
sys.stdout.flush()
timeout = 10
input = [my_socket, sys.stdin]
running = True;
while running:
    inputready,outputready,exceptready = select.select(input, [],[],timeout)

    for connection in inputready:
        if connection == sys.stdin:
            message = sys.stdin.readline()
            if message and len(message) > 1:
                my_socket.send(message)
                data = my_socket.recv(size)
                print data
                sys.stdout.write('> ')
                sys.stdout.flush()
            else:
                my_socket.close()
                running = False
        else:
            data = connection.recv(size)
            if data:
                print data
                sys.stdout.write('> ')
                sys.stdout.flush()
            else:
                connection.close()
