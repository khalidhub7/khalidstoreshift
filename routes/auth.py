#!/usr/bin/env python3
""" auth module """
from flask import session, redirect, url_for
from flask import current_app as app
from bson import ObjectId
import bcrypt


def isvalid_paswd(pswd):
    """
check if password is valid """
    if len(pswd) < 8:
        return False
    if not any(char.isdigit() for char in pswd):
        return False
    if not any(char.isalpha() for char in pswd):
        return False
    return True


def checkpswd(currentpswd, storedpswd):
    """
check if entered password validate user password """
    return bcrypt.checkpw(
        currentpswd.encode("utf-8"), storedpswd)


def isauthenticated():
    """ check if user already logged in"""
    user_id = session.get("user_id")
    if not user_id:
        return False
    return True


def isadmin():
    """Check if a user is an admin."""
    user_id = session.get("user_id")
    if not user_id:
        return False
    user = app.config["MONGO"].db.users.find_one(
        {"_id": ObjectId(user_id)})
    if user.get("role") == "admin":
        return True
    return False


def hashpass(password):
    """ hash text password """
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt())


def require_auth(route):
    """ require user auth for a route """
    def wrapped_func(*args, **kwargs):
        if not isauthenticated():
            return redirect(url_for("app_views.login"))
        return route(*args, **kwargs)
    return wrapped_func
