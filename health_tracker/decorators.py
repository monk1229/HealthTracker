from functools import wraps
from flask import session, request, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_name" not in session or len(session["user_name"]) < 1:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function