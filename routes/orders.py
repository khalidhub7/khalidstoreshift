#!/usr/bin/env python3
""" orders page """
from flask import current_app as app, render_template, abort
from datetime import datetime
from bson.objectid import ObjectId
from . import app_views


@app_views.route("/orders", methods=["GET"],
                 strict_slashes=False)
def display_orders():
    """ return orders list """
    mongo = app.config.get("MONGO")

    try:
        all_carts = list(mongo.db.cart.find())
        all_orders = []

        for cart in all_carts:
            user_id = str(cart.get("user_id"))

            if cart.get("products"):
                order = {"user_id": user_id,
                         "products": [],
                         "total_price": cart.get("total_price", 0),
                         "order_date": datetime.utcnow().strftime(
                             '%Y-%m-%dT%H:%M:%S'),
                         "status": "Delivered"}

                for item in cart["products"]:
                    product_id = item.get("product_id")
                    quantity = item.get("quantity")
                    price = item.get("price")

                    order["products"].append({
                        "product_id": product_id,
                        "quantity": quantity,
                        "price": price, })

                result = mongo.db.orders.insert_one(order)
                order["_id"] = str(result.inserted_id)
                mongo.db.cart.delete_one({"_id": cart["_id"]})
                all_orders.append(order)

        if not all_orders:
            return render_template("orders.html",
                                   message="No orders found.")

        return render_template("orders.html", orders=all_orders)

    except Exception as e:
        app.logger.error(f"An error occurred while fetching orders: {e}")
        abort(500)
