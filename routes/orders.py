#!/usr/bin/env python3
""" orders """
from flask import (current_app as app, request, session,
                   render_template, make_response,
                   render_template_string)
from datetime import datetime
from . import app_views
from .auth import isadmin, require_auth


@app_views.route("/orders", methods=["GET"],
                 strict_slashes=False)
@require_auth
def display_orders():
    """ return 'orders' list """
    mongo = app.config.get("MONGO")
    try:
        if not isadmin():
            return make_response(render_template_string("""
            <script>
                alert('You are not authorized to view this page.');
                window.location.href = '/khalid_store_shift/checkout';
            </script>
                                                        """), 403)

        allorders = list(mongo.db.orders.find())
        if not allorders:
            return render_template("orders.html",
                                   message="No orders found.")
        for order in allorders:
            order["_id"] = str(order["_id"])
        return render_template(
            "orders.html", orders=allorders)

    except Exception as e:
        app.logger.error(f"An error occurred while \
fetching orders: {e}")
        return make_response(render_template_string("""
        <script>
            alert('An error occurred while fetching orders.');
            window.location.href = '/khalid_store_shift/checkout';
        </script>
                                                    """), 500)


@app_views.route("/order/confirm", methods=["POST"],
                 strict_slashes=False)
def confirmorder():
    """ handle order confirmation """
    mongo = app.config.get("MONGO")

    try:
        full_name = request.form.get("full_name")
        address = request.form.get("address")
        payment_method = request.form.get("payment")

        user_id = session.get("user_id")
        cart = mongo.db.cart.find_one({"user_id": user_id})

        if not cart or not cart.get("products"):
            return make_response(render_template_string("""
            <script>
                alert('No products in the cart.');
                window.location.href = '/khalid_store_shift/checkout';
            </script>
                                                    """), 400)

        is_order_exist = mongo.db.orders.find_one(
            {"user_id": user_id, "status": "Pending"})

        order = {
            "user_id": user_id,
            "full_name": full_name,
            "address": address,
            "payment_method": payment_method,
            "products": [],
            "total_price": cart.get("total_price", 0),
            "order_date": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
            "status": "Pending",
        }

        for item in cart["products"]:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            price = item.get("price")

            order["products"].append({
                "product_id": product_id,
                "quantity": quantity,
                "price": price,
            })

        if is_order_exist:
            mongo.db.orders.update_one(
                {"_id": is_order_exist["_id"]},
                {"$set": order}
            )
        else:
            result = mongo.db.orders.insert_one(order)
            if not result.inserted_id:
                return make_response(render_template_string("""
                <script>
                    alert('Failed to confirm the order.');
                    window.location.href = '/khalid_store_shift/checkout';
                </script>
                                                    """), 500)

        # mongo.db.cart.delete_one({"_id": cart["_id"]})

        return make_response(render_template_string("""
        <script>
            alert('Order confirmed successfully!');
            window.location.href = '/khalid_store_shift/checkout';
        </script>
                                                    """), 200)

    except Exception as e:
        app.logger.error(f"An error occurred while \
confirming the order: {e}")
        return make_response(render_template_string("""
        <script>
            alert('An error occurred while confirming the order.');
            window.location.href = '/khalid_store_shift/checkout';
        </script>
                                                    """), 500)
