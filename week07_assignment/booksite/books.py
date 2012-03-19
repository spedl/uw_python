"""
Minimal Flask + forms demo

Send HTML page that echoes message from HTTP request
To get started, point browser at echo_flask.html
"""

from flask import Flask, render_template, request
from bookdb import BookDB



app = Flask(__name__)

app.debug = True # development only - remove on production machines

# View functions generate HTTP responses including HTML pages and headers
db = BookDB()

''' This function gets a dict of the ids and titles from the database and
passes it to the template.
'''
@app.route('/index.html/')
def index():
    return render_template('index.html', titles=db.titles())

''' This function takes a book id and gets the title info from the database as
a dict. This dict is passed to the template.
'''
@app.route('/book_details/<book_id>')
def detail(book_id=None):
    return render_template('detail.html', details=db.title_info(book_id))

if __name__ == '__main__':
    app.run()
