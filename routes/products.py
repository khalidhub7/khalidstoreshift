#!/usr/bin/env python3
""" products """
from flask import render_template, session, redirect
from . import app_views
from flask import current_app as app


@app_views.route("/products")
def products():
    """ all products page """
    mongo = app.config["MONGO"]
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/khalid_store_shift/login")
    products = mongo.db.products.find()
    return render_template(
        "products.html", products=products)


@app_views.route("/", methods=["GET"],
                 strict_slashes=False)
def home():
    """ home page """
    return render_template('landing.html')
