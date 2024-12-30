from flask import (request, session, make_response,
                   render_template, redirect,
                   render_template_string)
from . import app_views
from .auth import isvalid_paswd, hashpass
from . import db


@app_views.route("/register", methods=["GET", "POST"],
                 strict_slashes=False)
def register():
    """ Handles user registration. """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = db.find_user_by_email(email)
        if user:

            return make_response(render_template_string("""
        <script>
            alert("📧 Email already \
registered! Please log in to continue. 🔐");
            window.location.href = '/khalid_store_shift/register';
        </script>
                                                    """), 400)

        if not isvalid_paswd(password):
            return make_response(render_template_string("""
            <script>
                alert("Invalid password. It must be at least 8 characters \
long and contain both letters and numbers.");
                window.location.href = '/khalid_store_shift/register';
            </script>
            """), 400)

        password = hashpass(password)

        db.create_user(username, email, password)

        session["user_id"] = str(
            db.find_user_by_email(email)["_id"])
        return redirect("/khalid_store_shift/login")

    return render_template("register.html")
