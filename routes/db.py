#!/usr/bin/env python3
""" db module """
from flask import abort, redirect, make_response, render_template_string
from flask import current_app as app
import datetime
from bson import ObjectId
import os


def find_user_by_email(email):
    """ find a user by email """
    mongo = app.config["MONGO"]
    user = mongo.db.users.find_one(
        {"email": email})
    if user is None:
        return None
    return user


def create_user(username, email, password):
    """ create a new user in db """
    mongo = app.config["MONGO"]
    admins = os.getenv("admins", "").strip("[]").replace('"', '').split(",")
    role = "admin" if email in admins else "user"

    if email is None:
        return None
    new_user = mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "created_at": datetime.datetime.utcnow()
    })
    return new_user


def addtocart(mongo, user_id, product):
    """cart handler add update ..."""
    # abort(400, description="product out of stock! 📦")
    if product["stock"] <= 0:
        response = "product out of stock! 📦"
        return response

    cart = mongo.db.cart.find_one({"user_id": user_id})
    product_id = str(product["_id"])
    quantitytoadd = 1  # default quantity to add

    # create a new cart
    if not cart:
        cart = {
            "user_id": user_id,
            "products": [{
                "product_id": product_id,
                "quantity": quantitytoadd,
                "price": product["price"]
            }],
            "total_price": product["price"],
            "updated_at": datetime.datetime.utcnow()
        }
        mongo.db.cart.insert_one(cart)
        mongo.db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": -quantitytoadd}}
        )
    else:
        # check if product is already in the cart
        for item in cart["products"]:
            if item["product_id"] == product_id:
                oldquantity = item["quantity"]
                stock = oldquantity - (oldquantity + quantitytoadd)

                if product["stock"] + stock < 0:
                    response = "Not enough stock available! 📉"
                    return response
                item["quantity"] += quantitytoadd
                mongo.db.products.update_one(
                    {"_id": ObjectId(product_id)},
                    {"$inc": {"stock": stock}})
                break
        else:
            if product["stock"] < quantitytoadd:
                response = "Not enough stock available! 📉"
                return response

            cart["products"].append({
                "product_id": product_id,
                "quantity": quantitytoadd,
                "price": product["price"]})
            mongo.db.products.update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"stock": -quantitytoadd}})

        cart["total_price"] = sum(
            item["quantity"] * item["price"]
            for item in cart["products"])
        cart["updated_at"] = datetime.datetime.utcnow()

        # update cart in the db
        mongo.db.cart.update_one(
            {"_id": cart["_id"]}, {"$set": cart})
    return redirect("/products")
