"""Custom decorator to validate user token and add valid user data to config."""

from functools import wraps
from json import loads

from flask import request
from flask import current_app as app


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        token = request.headers.get("User-Authorization")
        if not token:
            return (
                {
                    "success": False,
                    "data": [],
                    "msg": "User-Authorization header is missing",
                },
                401,
            )

        if token != app.config["TOKEN"]:
            return (
                {
                    "success": False,
                    "data": [],
                    "msg": "User-Authorization header is invalid. Try to login again.",
                },
                401,
            )
        return f(*args, **kwargs)

    return wrapper
