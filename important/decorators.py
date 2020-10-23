from functools import wraps
from flask import (redirect, session, abort, request)
from dbManager import get_student_id, remove_token
from .connection import connection


def common_vars():
    status_update = dict()
    status_update['error'] = ''
    if 'error' in session:
        status_update['error'] = session['error']
        session.pop('error', None)
    status_update['success'] = ''
    if 'success' in session:
        status_update['success'] = session['success']
        session.pop('success', None)
    return status_update


def login_required(function):
    @wraps(function)
    def wrapper():
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
        status_update = common_vars()
        form_data = dict(request.form)
        if bool(form_data):
            return function(student_id=student_id, **status_update, **form_data)
        else:
            return function(student_id=student_id, **status_update)

    return wrapper


def login_not_required(function):
    @wraps(function)
    def wrapper():
        if 'adminError' in session:
            abort(500)
        if 'userToken' in session:
            return redirect('/')
        status_update = common_vars()
        form_data = dict(request.form)
        if bool(form_data):
            return function(**status_update, **form_data)
        else:
            return function(**status_update)

    return wrapper


def clear_session(function):
    @wraps(function)
    def wrapper():
        if 'userToken' in session:
            token = session['userToken']
            remove_token(token, connection)
        session.clear()
        return function()

    return wrapper
