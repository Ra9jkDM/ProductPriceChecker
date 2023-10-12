from functools import wraps
from flask_login import current_user

from models import User

def is_not_null(func):
    @wraps(func)
    def check(*args, **kwargs):
        if isinstance(current_user, User):
            return func(*args, **kwargs)
        return None
    return check

@is_not_null
def get_name():
    return current_user.firstname


@is_not_null
def get_id():
    return current_user.id

@is_not_null
def get_user_id():
    return current_user.id