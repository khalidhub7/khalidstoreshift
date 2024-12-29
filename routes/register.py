from flask import (request, session, make_response,
                   render_template, redirect,
                   render_template_string)
from . import app_views
import bcrypt
from . import db


@app_views.route("/register", methods=["GET", "POST"],
                 strict_slashes=False)
def register():
    """ Handles user registration. """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        user = db.find_user_by_email(email)
        if user:

            return make_response(render_template_string("""
        <script>
            alert("📧 Email already \
registered! Please log in to continue. 🔐");
            window.location.href = '/khalid_store_shift/register';
        </script>
                                                    """), 400)

        password = bcrypt.hashpw(
            request.form["password"].encode("utf-8"),
            bcrypt.gensalt())
        db.create_user(username, email, password)

        session["user_id"] = str(
            db.find_user_by_email(email)["_id"])
        return redirect("/khalid_store_shift/login")

    return render_template("register.html")
