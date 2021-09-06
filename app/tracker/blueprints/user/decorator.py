from functools import wraps
from flask import flash, redirect, url_for

from tracker.blueprints.user.models import CurrentUser


def role_required(*roles):
    """
    Does a user have permission to view this page?

    :param *roles: 1 or more allowed roles
    :return: Function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if CurrentUser().get_role() not in roles:
                flash('You do not have permission to do that.', 'error')
                return redirect(url_for('page.home'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
