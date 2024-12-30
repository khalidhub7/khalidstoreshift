#!/usr/bin/env python3
""" main file """
from flask import Flask
from flask_pymongo import PyMongo
from routes import app_views
import os
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# csrf = CSRFProtect(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce"
mongo = PyMongo(app)
app.config["MONGO"] = mongo
app.register_blueprint(app_views)


if __name__ == "__main__":
    app.run(debug=True)