#!/usr/bin/env python3
""" db module """
from flask import abort, redirect
from flask import current_app as app
import datetime
import bcrypt
from bson import ObjectId


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
    if email is None:
        return None
    new_user = mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": password,
        "created_at": datetime.datetime.utcnow()
    })
    return new_user


def isvalid_paswd(currentpswd, storedpswd):
    """
check if entered password validate user password """
    return bcrypt.checkpw(
        currentpswd.encode("utf-8"), storedpswd)


def addtocart(mongo, user_id, product):
    """cart handler add update ..."""
    if product["stock"] <= 0:
        abort(400, description="product out of stock! 📦")

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
                    abort(400, description="Not enough stock available! 📉")
                item["quantity"] += quantitytoadd
                mongo.db.products.update_one(
                    {"_id": ObjectId(product_id)},
                    {"$inc": {"stock": stock}})
                break
        else:
            if product["stock"] < quantitytoadd:
                abort(400, description="Not enough stock available! 📉")

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