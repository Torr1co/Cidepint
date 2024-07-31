""" This module contains the authentication function used to protect the app"""
from functools import wraps

from flask import abort, request, session
from werkzeug.exceptions import Forbidden

from src.dbo import permission_dbo, role_dbo
from src.web.utils import session as session_utils
from src.web.utils.api import error_response
from src.web.utils.jwt import jwt_auth


def is_logged_in():
    """Returns True if the user is logged in, False otherwise"""
    token = session.get("jwt_token")
    if not token:
        return False

    try:
        data = jwt_auth.decode(token)
        if not data:
            session.clear()
            raise RuntimeError("Token is invalid!")
    except RuntimeError:
        return False

    return True


def login_required(func):
    """Decorator that redirects to the login page if the user is not logged in"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return abort(401)

        return func(*args, **kwargs)

    return decorated_function


def validate_operation(operation):
    """
    Decorator that validates if the user has the permission to perform the given operation
    :param operation: The operation to validate
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token = session.get("jwt_token")
            if not token:
                return abort(401)
            data = jwt_auth.decode(token)
            if not data:
                return abort(401)

            user_role = session_utils.get_role()

            if not user_role:
                return abort(403)

            if not permission_dbo.check_permission(user_role, operation):
                return abort(403)

            return func(*args, **kwargs)

        return decorated_function

    return decorator


def token_required():
    """
    Decorator that validates if the user has a valid token
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return error_response()

            token = token.split("JWT ")
            if len(token) != 2:
                return error_response()

            data = jwt_auth.decode(token[1])
            if not data:
                return error_response()

            return func(*args, **kwargs)

        return decorated_function

    return decorator
