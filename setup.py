#!/usr/bin/env python3
""" setup db """
from pymongo import MongoClient
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "ecommerce"

products = [{"name": "Smartphone",
             "price": 699.99,
             "description": "High-end smartphone",
             "image_url": "images/smartphone-product.jpg",
             "stock": 5},
            {"name": "Laptop",
             "price": 1299.99,
             "description": "Lightweight laptop",
             "image_url": "images/laptop-product.jpg",
             "stock": 5},
            {"name": "Headphones",
             "price": 199.99,
             "description": "Noise-cancelling headphones",
             "image_url": "images/headphones-product.jpg",
             "stock": 5},
            {"name": "Smartwatch",
             "price": 299.99,
             "description": "Stylish smartwatch",
             "image_url": "images/smartwatch-product.jpg",
             "stock": 5},
            {"name": "Tablet",
             "price": 499.99,
             "description": "Portable tablet",
             "image_url": "images/tablet-product.jpg",
             "stock": 5},
            {"name": "Camera",
             "price": 899.99,
             "description": "High-resolution camera",
             "image_url": "images/camera-product.jpg",
             "stock": 5}]


def setup_database():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    client.drop_database(DATABASE_NAME)
    print(f"Database '{DATABASE_NAME}' cleared.")
    db.products.insert_many(products)
    print("'products' collection created and populated.")
    db.create_collection("users")
    print("'users' collection created.")
    db.create_collection("cart")
    print("'cart' collection created.")
    db.create_collection("orders")
    print("'orders' collection created.")
    client.close()
    print("Database setup completed.")


if __name__ == "__main__":
    setup_database()