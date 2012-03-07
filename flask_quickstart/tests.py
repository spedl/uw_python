from flask import request

with app.test_request_context('/hello', method='POST'):
    assert request.path == '/hello'
    assert request.method == 'POST'


# Another option is passing a whole WSGI environment to the method
with app.request_context(environ):
    assert request.method == 'POST'
