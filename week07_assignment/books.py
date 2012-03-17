"""
Minimal Flask + forms demo

Send HTML page that echoes message from HTTP request
To get started, point browser at echo_flask.html
"""

from flask import Flask, render_template, request
from bookdb import BookDB



app = Flask(__name__)


detail_template = """
<html>
<head>
<title> %s </title>
</head>
<body>
Title: %s <br />
ISBN: %s <br />
Publisher: %s <br />
Author: %s <br />
</body>
</html>
"""

index_template = """
<html>
<head>
<title> Library </title>
</head>
<body>
<a href="/book/%(id)s">%(title)s</a><br />
<a href="/book/%(id)s">%(title)s</a><br />
<a href="/book/%(id)s">%(title)s</a><br />
<a href="/book/%(id)s">%(title)s</a><br />
<a href="/book/%(id)s">%(title)s</a><br />
</body>
</html>
"""


app.debug = True # development only - remove on production machines

# View functions generate HTTP responses including HTML pages and headers

''' This function needs to get all the titles or set up the template to get all
the titles'''
@app.route('/index.html/')
def index():
    db = BookDB()
    book_dict = db.titles()
    import pdb; pdb.set_trace()
    return index_template % book_dict

''' This function needs to send the book_id to the template '''
@app.route('/book/<book_id>')
def detail(book_id=None):
    db = BookDB()
    return detail_template % (db.title_info(book_id))

def application(environ, start_response):
    global messages
    status = '200 OK'
    response_headers = [('Content_type', 'text/HTML')]
    start_response(status, response_headers)
    # send different page depending on URL path
    path = environ['PATH_INFO'] 
    if path == '/echo_wsgi.html':
        page = form_page
    elif path == '/echo_wsgi.py':
        # get message from URL query string, parse_qs returns a list for each key
        message = \
            urlparse.parse_qs(environ['QUERY_STRING'])['message'][0]
        messages = ('%s<br>\n' % message) + messages # insert at head
        page = message_template % messages
    else:
        page = notfound_template % path
    return [ page ] # list of strings - must return iterable, not just a string

if __name__ == '__main__':
    app.run()

