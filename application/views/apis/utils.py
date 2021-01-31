from flask import escape
from application.models.models import User
from base64 import b64decode


def AuthorizeRequest(headers):
    if not "Authorization" in headers:
        return False

    token = headers["Authorization"]
    token = escape(token)
    token_str = str(token).encode("ascii")
    missing_padding = len(token_str) % 4
    if missing_padding:
        return False

    token = b64decode(token_str)
    user = User.query.filter_by(token=token)
    if not user.count() > 0:
        return False

    return user.first()


def getPasswordResetUser(headers, email, code):
    if not "Authorization" in headers:
        return False

    token = headers["Authorization"]
    token = escape(token)
    token_str = str(token).encode("ascii")
    missing_padding = len(token_str) % 4
    if missing_padding:
        return False

    token = b64decode(token_str)
    user = User.query.filter_by(reset_token=token, email=email, reset_code=code)
    if not user.count() > 0:
        return False

    return user.first()


def getPasswordResetUserWithoutCode(headers, email):
    if not "Authorization" in headers:
        return False

    token = headers["Authorization"]
    token = escape(token)
    token_str = str(token).encode("ascii")
    missing_padding = len(token_str) % 4
    if missing_padding:
        return False

    token = b64decode(token_str)
    user = User.query.filter_by(reset_token=token, email=email)
    if not user.count() > 0:
        return False

    return user.first()


notLoggedIn = {"isLoggedIn": False, "message": "you are not logged in"}
