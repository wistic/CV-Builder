from flask import (Flask, render_template, redirect, session, abort, request)
from flask_wtf.csrf import CSRFProtect
import os

from important import *
from utility import *
from dbManager import *

app = Flask(__name__)
app.secret_key = os.urandom(16)
csrf = CSRFProtect(app)


@app.route('/')
@login_required
def homepage(**kwargs):
    student_data = get_student_data(kwargs['student_id'], connection)
    return render_template('index.html', student_data=student_data)


@app.route('/login', methods=['GET', 'POST'])
@login_not_required
def login(**kwargs):
    if request.method == 'POST':
        status_code, description = verify_login(kwargs['student_id'], kwargs['password'], connection)
        if status_code is Status.SUCCESS:
            random_session_hash = get_random_hash()
            session['userToken'] = random_session_hash
            insert_token(random_session_hash, kwargs['student_id'], connection)
            return redirect('/')
        elif status_code is Status.ERROR:
            session['adminError'] = description
            abort(500)
        else:
            session['error'] = description
            return redirect('/login')
    return render_template('login.html', error=kwargs['error'], success=kwargs['success'])


@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password(**kwargs):
    if request.method == 'POST':
        status_code, description = change_password(kwargs['student_id'], kwargs['current_password'],
                                                   kwargs['new_password'],
                                                   kwargs['confirm_new_password'], connection)
        if status_code is Status.SUCCESS:
            session['success'] = description
            return redirect('/update_password')
        elif status_code is Status.ERROR:
            session['adminError'] = description
            abort(500)
        else:
            session['error'] = description
            return redirect('/update_password')
    return render_template('update_password.html', error=kwargs['error'], success=kwargs['success'])


@app.route('/logout')
@login_required
def logout(**kwargs):
    token = session['userToken']
    session.pop('userToken', None)
    remove_token(token, connection)
    session['success'] = "You are now successfully logged out."
    return redirect('/login')


@app.route('/reset')
@clear_session
def reset_session():
    return redirect('/login')


@app.errorhandler(400)
@clear_session
def handle_csrf_error(e):
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
@login_required
def dashboard(**kwargs):
    student_data = get_student_data(kwargs['student_id'], connection)
    return render_template("dashboard.html", student_data=student_data)
