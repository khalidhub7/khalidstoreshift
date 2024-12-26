#!/usr/bin/env python3
""" user login logout """
from flask import (request, session, redirect,
                   url_for, abort, render_template)
from . import app_views
from . import db


@app_views.route("/login", methods=["GET", "POST"],
                 strict_slashes=False)
def login():
    """ login """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = db.find_user_by_email(email)
        if user and db.isvalid_paswd(
                password, user['password']):
            session["user_id"] = str(user["_id"])
            return redirect(url_for("app_views.products"))

        abort(400, description="Invalid \
credentials! Please try again. 🔑")
    return render_template('/login.html')



@app_views.route("/logout", methods=["GET"],
                 strict_slashes=False)
def logout():
    """ logout """
    session.pop("user_id", None)
    return redirect(url_for("app_views.login"))
