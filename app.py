# Import from pip packages
from flask import (Flask, render_template, redirect, request, session, abort)
from flask_wtf.csrf import CSRFProtect
import pymysql.cursors
import os

# Import from local packages
from utility import *
from dbManager import *
from config import config

# App initialization
app = Flask(__name__)
app.secret_key = os.urandom(16)
csrf = CSRFProtect(app)

# Connection variables initialization
try:
    mysql_password = os.environ['MYSQL_PASSWORD']
except KeyError:
    mysql_password = config['mysql_password']
try:
    mysql_host = os.environ['MYSQL_HOST']
except KeyError:
    mysql_host = config['mysql_host']
try:
    mysql_user = os.environ['MYSQL_USER']
except KeyError:
    mysql_user = config['mysql_user']
try:
    mysql_db = os.environ['MYSQL_DB']
except KeyError:
    mysql_db = config['mysql_db']
try:
    mysql_charset = os.environ['MYSQL_CHARSET']
except KeyError:
    mysql_charset = config['mysql_charset']

# Mysql connection initialization
try:
    connection = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 charset=mysql_charset,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True,
                                 connect_timeout=100)
except pymysql.Error:
    logger.critical('Unable to connect to the database.')
    connection = ''

remove_all_tokens(connection)  # Remove all sessions


# BEGIN Route definition #
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
    student_id = get_student_id(session['userToken'], connection)
    if student_id == -1:
        session['error'] = "You must login again to access the site."
        session.pop('userToken', None)
        return redirect('/login')
    student_data = get_student_data(student_id, connection)
    return render_template('index.html', success=success, student_data=student_data)


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


@app.route('/update_password')
def update_password():
    if 'adminError' in session:
        abort(500)
    if 'userToken' not in session:
        session['error'] = "You must login to access the site."
        return redirect('/login')
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error', None)
    success = ''
    if 'success' in session:
        success = session['success']
        session.pop('success', None)
    return render_template('update_password.html', error=error, success=success)


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
        insert_token(random_session_hash, enrollment_no, connection)
        return redirect('/')
    elif status == "Database inconsistency - Call Admin":
        session['adminError'] = status
        abort(500)
    else:
        session['error'] = status
        return redirect('/login')


@app.route('/handle_update_password', methods=['POST'])
def handle_update_password():
    if 'adminError' in session:
        abort(500)
    if 'userToken' not in session:
        session['error'] = "You must login to access the site."
        return redirect('/login')

    try:
        current_password = request.form['current_password']
    except KeyError:
        current_password = ''
    try:
        new_password = request.form['new_password']
    except KeyError:
        new_password = ''
    try:
        confirm_password = request.form['confirm_password']
    except KeyError:
        confirm_password = ''

    if connection == '':
        session['adminError'] = "Database inconsistency - Call Admin"
        abort(500)
    enrollment_no = get_student_id(session['userToken'], connection)
    if enrollment_no == -1:
        session['error'] = "You must login again to access the site."
        session.pop('userToken', None)
        return redirect('/login')

    status = change_password(enrollment_no, current_password, new_password, confirm_password, connection)
    if status == "Password updated successfully":
        session['success'] = status
        return redirect('/update_password')
    elif status == "Database inconsistency - Call Admin":
        session['adminError'] = status
        abort(500)
    else:
        session['error'] = status
        return redirect('/update_password')


@app.route('/logout')
def logout():
    if 'adminError' in session:
        abort(500)
    if 'userToken' not in session:
        session['error'] = "You must login first"
        return redirect('/login')
    token = session['userToken']
    session.pop('userToken', None)
    remove_token(token, connection)
    session['success'] = "You are now successfully logged out."
    return redirect('/login')


@app.route('/reset')
def reset_session():
    if 'userToken' in session:
        token = session['userToken']
        remove_token(token, connection)
    session.clear()
    return redirect('/login')


@app.errorhandler(400)
def handle_csrf_error(e):
    if 'userToken' in session:
        token = session['userToken']
        remove_token(token, connection)
    session.clear()
    logger.warning(e.description)
    return render_template('csrf_error.html'), 400


@app.errorhandler(404)
def handle_404(e):
    logger.warning(e.description)
    return render_template("404_error.html"), 404


@app.errorhandler(500)
def handle_500(e):
    logger.warning(e.description)
    return render_template("500_error.html"), 500


@app.route('/dashboard')
def dashboard():
    if 'adminError' in session:
        abort(500)
    if 'userToken' not in session:
        session['error'] = "You must login to access the site."
        return redirect('/login')
    student_id = get_student_id(session['userToken'], connection)
    if student_id == -1:
        session['error'] = "You must login again to access the site."
        session.pop('userToken', None)
        return redirect('/login')
    student_data = get_student_data(student_id, connection)
    return render_template("dashboard.html", student_data=student_data)
