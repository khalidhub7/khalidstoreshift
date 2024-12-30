#!/usr/bin/env python3
""" user login logout """
from flask import (request, session, redirect,
                   url_for, make_response, render_template,
                   render_template_string)
from .auth import isauthenticated, checkpswd
from . import app_views
from . import db


@app_views.route("/login", methods=["GET", "POST"],
                 strict_slashes=False)
def login():
    """ login """
    if isauthenticated():
        return redirect(url_for("app_views.products"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = db.find_user_by_email(email)
        if user and checkpswd(
                password, user['password']):
            session["user_id"] = str(user["_id"])
            return redirect(url_for("app_views.products"))

        return make_response(render_template_string("""
        <script>
            alert("Invalid \
credentials! Please try again. 🔑");
            window.location.href = '/khalid_store_shift/login';
        </script>
                                                    """), 400)
    return render_template('/login.html')


@app_views.route("/logout", methods=["GET"],
                 strict_slashes=False)
def logout():
    """ logout """
    session.pop("user_id", None)
    return make_response(render_template_string("""
        <script type="text/javascript">
            alert("You have logged out successfully! 👍👋");
            window.location.href = '/khalid_store_shift';
        </script>
    """), 200)
