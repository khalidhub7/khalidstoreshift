#!/usr/bin/env python3
"""
checkout page """
from flask import (url_for, session, redirect,
                   render_template)
from . import app_views
from flask import current_app as app


@app_views.route("/checkout", methods=["GET"],
                 strict_slashes=False)
def checkout():
    """ checkout process"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("app_views.login"))

    mongo = app.config["MONGO"]
    cart = mongo.db.cart.find_one(
        {"user_id": user_id})

    if not cart or not cart.get("products"):
        return redirect("/cart")
    return render_template("checkout.html", cart=cart)