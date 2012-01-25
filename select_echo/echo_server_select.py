#!/usr/bin/python
"""
Based on Daniel Zappala's http://ilab.cs.byu.edu/python/code/echoserver-select.py
Add print statements to show what's going on.
Use SO_REUSEADDR to avoid 'Address already in use' errors
Add timeout
make style similar to our recho_client

An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import time
import datetime

# No host indicates localhost
host = ''
port = 50003

# If a port is specified the code accepts it here
if len(sys.argv) > 1:
    port = int(sys.argv[1])

backlog = 5
size = 1024     # buffer

# Creates a socket instance that is of the address family IPv4
# and connection-oriented (streaming)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Release listener socket immediately when program exits, 
# avoid socket.error: [Errno 48] Address already in use
# the level - SOL_SOCKET - sets connection at socket level
# the option - SO_REUSEADDR allows reuse of the local address
# the value - 1 indicates enabling of the option?
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host,port))

print 'echo_server listening on port %s, to exit type return ' % port
server.listen(backlog)

timeout = 10 # seconds
input = [server,sys.stdin]
output = []
message_dict = {}
running = True
while running:
    inputready,outputready,exceptready = select.select(input, [],[],timeout)

    if not inputready:
        print 'Server running at %s' datetime.datetime.now()

    for s in inputready:

        if s == server:
            # handle the server socket
            client, address = server.accept()
            input.append(client)
            output.append(client)
            message_dict[client] = []
            print 'accepted connection from', address

        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = False
            print 'Input %s from stdin, exiting.' % junk.strip('\n')

        elif s: # client socket
            data = s.recv(size)
            print '%s: %s' % (s.getpeername(), data.strip('\n'))
            if data:
                message = '(spedl_server) %s: %s\n' % (s.getpeername(),
                        data.strip('\n'))
                for o in output:
                    o.send(message);
            else:
                s.close()
                print 'closed connection'
                input.remove(s)
                output.remove(s)

    #for s in outputready:
    #    messages = message_dict[s]
    #    for i in range(len(messages)):
    #        s.send(messages.pop())

s.close()
