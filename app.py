from flask import (Flask, render_template, redirect, request, session)
from flask_wtf.csrf import (CSRFProtect, CSRFError)
import pymysql.cursors
import os

from utility import logger, get_random_hash
from db import verify_login
from config import config

app = Flask(__name__)
app.secret_key = config['secret_key']
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
    exit(0)


@app.route('/')
@app.route('/dashboard')
def hello_world():
    if 'userToken' not in session:
        session['error'] = "You must login to access the site."
        return redirect('/login')
    return render_template('dashboard.html')


@app.route('/login')
def login():
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
    status = verify_login(enrollment_no, password, connection)
    if status == "Success":
        session['success'] = status
        random_session_hash = get_random_hash()
        session['userToken'] = random_session_hash
        return redirect('/')
    elif status == "Database inconsistency":
        session['adminError'] = status
        return redirect('/error')
    else:
        session['error'] = status
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('userToken', None)
    session['success'] = "You are now successfully logged out."
    return redirect('/login')


#
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400
