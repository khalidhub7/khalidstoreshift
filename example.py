# Collection: users
{
    "_id": "unique_user_id",          # Auto-generated ID
    "username": "user123",            # Unique username
    "email": "user@example.com",      # Unique email
    "password": "hashed_password",    # Hashed password
    "created_at": "2024-12-15T12:00:00"  # Account creation timestamp
}

# Collection: products
{
    "_id": "unique_product_id",      # Unique product ID
    "name": "Product Name",          # Product name
    "description": "Product details",
    "price": 99.99,                  # Product price
    "stock": 50,                     # Available stock
    "created_at": "2024-12-15T12:00:00"  # Product added timestamp
}

# Collection: cart
{
    "_id": "cart_id",                # Cart ID
    "user_id": "unique_user_id",     # User reference
    "products": [
        {
            "product_id": "unique_product_id",  # Product reference
            "quantity": 2,                     # Quantity in cart
            "price": 99.99                     # Price at add to cart time
        }
    ],
    "total_price": 199.98,            # Total cart price
    "updated_at": "2024-12-15T12:30:00"  # Last update timestamp
}

# Collection: orders
{
    "_id": "order_id",               # Order ID
    "user_id": "unique_user_id",     # User reference
    "products": [
        {
            "product_id": "unique_product_id",  # Product reference
            "quantity": 2,                     # Quantity purchased
            "price": 99.99                     # Price at time of purchase
        }
    ],
    "total_price": 199.98,            # Total order price
    "order_date": "2024-12-15T12:30:00",  # Order timestamp
    "status": "Delivered"             # Order status (e.g., Delivered)
}
