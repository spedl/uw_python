#
# ws30 -- the thirty minute web server
# author: Wilhelm Fitzpatrick (rafial@well.com)
# date: August 3rd, 2002
# version: 1.0
#
# Written after attending a Dave Thomas talk at PNSS and hearing about
# his "write a web server in Ruby in one hour" challenge.
#
# Actual time spent:
#  30 minutes reading socket man page
#  30 minutes coding to first page fetched
#   3 hours making it prettier & more pythonic
#
# updated for UW Internet Programming in Python, by Brian Dorsey
# updated by Jon Jacky: in defaults, replace '127.0.0.1' with ''
#  to allow connection from other hosts besides localhost
#

import os, socket, sys, datetime

defaults = ['', '8080']  # '127.0.0.1' here limits connections to localhost
mime_types = {'.jpg' : 'image/jpg', 
             '.gif' : 'image/gif', 
             '.png' : 'image/png',
             '.html' : 'text/html', 
             '.pdf' : 'application/pdf'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""

DIRECTORY_LINE = '<a href="%s">%s</a><br>'

def server_socket(host, port):
    ''' This method initializes a socket object and binds to the host and port
    specified before setting it to listen at that location. The socket object
    is then returned.'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    return s

# Unfinished documentation
def listen(s):
    ''' This method takes a socket object and 
    '''
    connection, client = s.accept()
    return connection.makefile('r+')

# Unfinished documentation
def get_request(stream):
    ''' This method takes a socket stream and reads it line by line, printing
    each line to the console. And then >>>>>>>>what does line.strip() remove?
    This method processes HTTP requests from a client and returns the
    address(path) to the requested resource.
    '''
    method = None
    while True:
        line = stream.readline()
        print line
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
    return uri

# What does os.listdir do?
def list_directory(uri):
    ''' This method takes a path to a resource and then inserts the uri string
    into the DIRECTORY_LISTING string as both the title and the link. It also
    takes the list of items in the directory pointed to by the uri (path) and
    joins them into a string to be passed in as the third string argument to
    DIRECTORY_LISTING. <<<< This is my guess about os.listdir().
    '''
    entries = os.listdir('.' + uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))

def get_file(path):
    ''' This method takes a path to a file and returns the contents as a
    string. I think.
    '''
    f = open(path)
    try: 
        return f.read()
    finally: 
        f.close()

# Not yet implemented. How to run?
def get_output(path):
    ''' This method takes a path to a .py file, runs it and returns the output.
    '''
    return os.popen('python ' + path).read()

def get_content(uri):
    ''' This method takes in a uri (path to resource) and determines whether it
    is a path to a file or a directory. 

    -- If a file, if the filename ends with .py it calls get_output() and
    returns that output as text along with a 200 response. Otherwise, it calls
    get_mime() to get the type for the header, and get_file() to get the
    contents. It then returns these two parts along with a 200 response.

    -- If a directory, it returns 200, with a text type, and calls list_directory
    to get the a string listing of all the files in the directory.

    -- If it is a directory but the path does not end with '/', it returns a
    300 along with the uri, indicating that the resource is missing.

    -- If it is not found, a 404 error is returned along with the uri.
    Indicating that        

    -- If an IOError is thrown it is returns with a 404.
    '''
    print 'fetching:', uri
    try:
        path = '.' + uri
        if (uri.endswith('date.html')):
                return (200, 'text/plain', 'Check out the time, bro!: %s' %
                             datetime.datetime.now())
        if os.path.isfile(path):
            if (uri.endswith('.py')):
                return (200, 'text/html', get_output(path))
            else:
                return (200, get_mime(uri), get_file(path))
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri))
            else:
                return (301, uri + '/')
        else: return (404, uri)
    except IOError, e:
        return (404, e)

# What does os.path.splitext do?                     
def get_mime(uri):
    ''' This method attempts to get the mime type from the uri by calling
    os.path.splitext() and passing that value into the mime_types dictionary
    defined at the top of the file.
    '''
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):
    ''' This method takes a socket stream and a content list and writes the
    content out to the stream. Something abou the way it's passed to write           
    -- response is a dictionary and content is a list of length 3.
    [RESPONSE CODE, MIME_TYPE, RESOURCE] where resource is text or image?
    The code determines the format of the page that is returned. The rest of
    the values replace %s placeholders in the page template.
    '''
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    ''' This is the part of the program that runs when the it is called from
    the command line. Any arguments that are passed in are placed in the args
    list and the number of arguments is stored in the nargs variable.
    Not sure about the host, port line                  
    server_socket is called to setup the socket on the specified host and port.
    '''
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            send_response(stream, get_content(get_request(stream)))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

