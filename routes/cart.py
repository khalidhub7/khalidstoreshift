#!/usr/bin/env python3
""" cart module """
from flask import (session, request, redirect,
                   url_for, render_template, abort)
from . import app_views
from flask import current_app as app
from bson import ObjectId
import datetime
from . import db


@app_views.route("/cart/add", methods=["POST"],
                 strict_slashes=False)
def add_to_cart():
    """ add product to user's cart """
    mongo = app.config["MONGO"]
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("app_views.products"))
    product_id = request.form.get("product_id")
    if not product_id:
        return redirect(url_for("app_views.products"))
    try:
        product = mongo.db.products.find_one(
            {"_id": ObjectId(product_id)})
    except Exception as e:
        return redirect(url_for("app_views.products"))
    if not product:
        return redirect(url_for("app_views.products"))
    db.addtocart(mongo, user_id, product)
    return redirect(url_for("app_views.products"))


@app_views.route("/cart")
def cart():
    """ cart page """
    mongo = app.config["MONGO"]
    user_id = session.get("user_id")
    if not user_id:
        return redirect(
            url_for("app_views.login"))
    cart = mongo.db.cart.find_one(
        {"user_id": user_id})
    return render_template("cart.html", cart=cart)


@app_views.route("/cart/remove", methods=["POST"],
                 strict_slashes=False)
def remove_from_cart():
    """ remove item from cart """
    mongo = app.config["MONGO"]
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("app_views.login"))
    product_id = request.form["product_id"]
    cart = mongo.db.cart.find_one({"user_id": user_id})
    if cart:
        # update products (by remove item)
        cart['products'] = [
            item for item in cart['products']
            if item["product_id"] != product_id]
        # total price
        cart["total_price"] = sum(
            item["quantity"] * item["price"]
            for item in cart["products"])
        cart["updated_at"] = datetime.datetime.utcnow()
        if not cart["products"]:
            # delete cart if empty
            mongo.db.cart.delete_one({"_id": cart["_id"]})
        else:
            mongo.db.cart.update_one(
                {"_id": cart["_id"]}, {"$set": cart})
    return redirect(url_for("app_views.cart"))


@app_views.route("/cart/update", methods=["POST"],
                 strict_slashes=False)
def update_cart():
    """ update cart items """
    mongo = app.config["MONGO"]
    user_id = session.get("user_id")
    product_id = request.form["product_id"]
    newquantity = int(request.form["quantity"])
    if not user_id:
        return redirect(url_for("app_views.login"))
    cart = mongo.db.cart.find_one(
        {"user_id": user_id})
    if cart:
        for item in cart["products"]:
            if item["product_id"] == product_id:
                oldquantity = item["quantity"]
                # calculate stock change
                stock = oldquantity - newquantity
                product = mongo.db.products.find_one(
                    {"_id": ObjectId(product_id)})
                if product["stock"] + stock < 0:
                    abort(400, description="Not enough \
stock available.")
                item["quantity"] = newquantity
                mongo.db.products.update_one(
                    {"_id": ObjectId(product_id)},
                    {"$inc": {"stock": stock}}
                )
                break
        cart["total_price"] = sum(item["quantity"] * item["price"]
                                  for item in cart["products"])
        cart["updated_at"] = datetime.datetime.utcnow()
        mongo.db.cart.update_one(
            {"_id": cart["_id"]}, {"$set": cart})
    return redirect(url_for("app_views.cart"))
