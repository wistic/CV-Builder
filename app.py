from flask import (Flask, render_template, redirect, request, session, abort)
from flask_wtf.csrf import (CSRFProtect, CSRFError)
import pymysql.cursors
import os

from utility import logger, get_random_hash
from db import verify_login
from config import config

app = Flask(__name__)
app.secret_key = os.urandom(16)
csrf = CSRFProtect(app)
logger.debug('Started')
try:
    mysql_password = os.environ['MYSQLPASSWORD']
except KeyError:
    mysql_password = config['mysql_password']

try:
    connection = pymysql.connect(host=config['host'],
                                 user=config['user'],
                                 password=mysql_password,
                                 db=config['database'],
                                 charset=config['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
except pymysql.Error:
    logger.critical('Unable to connect to the database.')
    connection = ''


@app.route('/')
def homepage():
    if 'adminError' in session:
        abort(500)
    if 'userToken' not in session:
        session['error'] = "You must login to access the site."
        return redirect('/login')
    success = ''
    if 'success' in session:
        success = session['success']
        session.pop('success', None)
    else:
        pass
        # TODO Validate
    return render_template('index.html', success=success)


@app.route('/login')
def login():
    if 'adminError' in session:
        abort(500)
    if 'userToken' in session:
        return redirect('/')
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error', None)
    success = ''
    if 'success' in session:
        success = session['success']
        session.pop('success', None)
    return render_template('login.html', error=error, success=success)


@app.route('/handle_login', methods=['POST'])
def handle_login():
    if 'adminError' in session:
        abort(500)
    if 'userToken' in session:
        return redirect('/')
    try:
        enrollment_no = request.form['enrollment_no']
    except KeyError:
        enrollment_no = ''
    try:
        password = request.form['password']
    except KeyError:
        password = ''
    if connection == '':
        session['adminError'] = "Database inconsistency - Call Admin"
        abort(500)
    status = verify_login(enrollment_no, password, connection)
    if status == "Login Success":
        session['success'] = status
        random_session_hash = get_random_hash()
        session['userToken'] = random_session_hash
        # TODO Insert into db
        return redirect('/')
    elif status == "Database inconsistency - Call Admin":
        session['adminError'] = status
        abort(500)
    else:
        session['error'] = status
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'adminError' in session:
        abort(500)
    if 'userToken' not in session:
        session['error'] = "You must login first"
        return redirect('/login')
    session.pop('userToken', None)
    # TODO Remove from db
    session['success'] = "You are now successfully logged out."
    return redirect('/login')


@app.route('/reset')
def reset_session():
    session.clear()
    # TODO Remove from db
    return redirect('/login')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    session.clear()
    # TODO Remove from db
    return render_template('csrf_error.html', reason=e.description), 400


@app.errorhandler(404)
def handle_404(e):
    return render_template("pagenotfound.html"), 404


@app.errorhandler(500)
def handle_500(e):
    return render_template("internalerror.html"), 500
