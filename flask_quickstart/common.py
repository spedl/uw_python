from flask import request, render_template

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
            # this is executed if the request method was GET or the credentials
            # were invalid


# File Uploads
from werkzeug import secure_filename

@app.route('/upload', method=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))


# Reading cookies

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a KeyError if the
    # cookie is missing.

# Storing cookies

@app.route('/')
def index():
    resp = make_response(render_template(response.html))
    #resp = make_response(Template(u'{{ username }}'))
    resp.set_cookies('username', 'the username')
    return resp

# Redirects and Errors with a pointless example
# ------
# The user is redirected from the index to page that they cannot access.
# 401 means access denied.
from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

# Customize the error page

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# Getting ahold of the response obect and modifying it
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp














