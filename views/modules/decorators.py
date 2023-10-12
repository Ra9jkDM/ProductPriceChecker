from functools import wraps

from flask import render_template, url_for, redirect
from flask_login import current_user

from database import role

def is_not_authenticated(func):
    @wraps(func)
    def check_authentication(*args, **kwargs):
        if not current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("view.index"))
    return check_authentication

def is_admin(func):
    @wraps(func)
    def check_role(*args, **kwargs):
        if role.is_admin(current_user):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("view.index"))
    return check_role
