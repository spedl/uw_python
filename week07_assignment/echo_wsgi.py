"""
Minimal WSGI + forms demo, with persistence

Send HTML page that echoes message from HTTP request,
also shows all messages received since startup.

To get started, point browser at echo_wsgi.html

Based on example in PEP 333, then add path and query processing
"""

import urlparse
from bookdb import BookDB

# send one of these pages, depending on URL path

notfound_template = """
<html>
<head>
<title>404 Not Found</title>
</head>
<body>
404 %s not found
</form>
</body>
</html>
"""

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
<a href="/detail.html/?book_id=%s">%s</a><br />
<a href="/detail.html/?book_id=%s">%s</a><br />
<a href="/detail.html/?book_id=%s">%s</a><br />
<a href="/detail.html/?book_id=%s">%s</a><br />
<a href="/detail.html/?book_id=%s">%s</a><br />
</body>
</html>
"""

# must be named 'application' to work with our wsgi simple server
def application(environ, start_response):
    global messages
    status = '200 OK'
    response_headers = [('Content_type', 'text/HTML')]
    start_response(status, response_headers)
    # send different page depending on URL path
    path = environ['PATH_INFO'] 
    db = BookDB()
    if path == '/index.html':
        book_list = db.titles()
        strings = []
        for book in book_list:
            book_id = book['id']
            book_title = book['title']
            strings.append(book_id)
            strings.append(book_title)
        page = index_template % (strings[0],strings[1],strings[2],
                                 strings[3],strings[4],strings[5],
                                 strings[6],strings[7],strings[8],
                                 strings[9])
    elif path == '/detail.html/':
        book_id = \
            urlparse.parse_qs(environ['QUERY_STRING'])['book_id'][0]
        book_info = db.title_info(book_id)
        page = detail_template % (book_info['title'], book_info['title'], book_info['isbn'], \
                book_info['publisher'], book_info['author'])
    else:
        page = notfound_template % path
    return [ page ] # list of strings - must return iterable, not just a string
