"""
recho client, usage:

 python recho_client.py <host> <port>

Both host and port are optional, defaults: localhost 50000
host must be present if you want to provide port

Prompt user for each message to send
Repeat seding messages until user enters empty string
"""

import socket
import sys

host = 'localhost'
port = 55555
size = 1024

nargs = len(sys.argv)
if nargs > 1:
    host = sys.argv[1]
if nargs > 2:
    port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM)
s.connect((host,port))
print 'Connection accepted by (%s,%s)' % (host, port)
while True:
    message = raw_input("> ")
    if message:
        s.send(message)
        data = s.recv(size)
        print data
    else:
        s.close()
        break

