#!/usr/bin/env python3
""" main file """
from flask import Flask
from flask_pymongo import PyMongo
from routes import app_views
app = Flask(__name__)
app.secret_key = "khalid_key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce"
mongo = PyMongo(app)
app.config["MONGO"] = mongo
app.register_blueprint(app_views)


if __name__ == "__main__":
    app.run(debug=True)