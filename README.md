# Khalid Store Shift
A simple e-commerce platform built using Flask, MongoDB, and Python. This project includes user authentication, cart management, product display, and order handling functionality. It allows users to register, log in, add products to their cart, and place orders.

## Features
- **User Authentication**: Users can register, log in, and log out. Passwords are hashed and validated.
- **Product Management**: Display a list of products, and allow users to add them to their cart and update/remove items.
- **Cart Management**: Users can view, add, update, and remove products from their cart.
- **Order Management**: Users can proceed to checkout and confirm orders. Admin users can view all orders.
- **Role-based Access Control**: Admin users have special privileges to view and manage orders, while regular users can only manage their own carts and orders.

## Installation
To run the project locally, follow the steps below:

### Prerequisites
- Python 3.x
- Flask
- MongoDB (local or hosted instance)
- Redis (optional, if needed for session management)
- Virtual Environment (recommended)

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/khalidstoreshift.git
    cd khalidstoreshift
    ```
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables:
    - Set the `MONGO_URI` variable to connect to your MongoDB instance (local or remote).
    - (Optional) Set the `admins` variable to specify admin email addresses for role-based access.

5. Run the application:
    ```bash
    python app.py
    ```
    Access the application at `http://127.0.0.1:5000/`

## Project Structure
- **auth.py**: Contains authentication-related functions such as password validation and checking user login status.
- **cart.py**: Contains routes for adding, updating, and removing items from the user's cart.
- **checkout.py**: Manages the checkout process where users confirm their orders.
- **db.py**: Handles database interactions such as finding users, creating users, and managing cart operations.
- **login.py**: Handles user login and logout routes.
- **orders.py**: Manages orders for admin and user-related functionality.
- **products.py**: Displays all products for users to browse and add to their cart.
- **register.py**: Handles user registration, including validation and creating a new user.

## Frontend
The frontend consists of HTML and CSS files located in the `templates` directory. The pages include:
- **landing.html**: The home page.
- **login.html**: The login page.
- **register.html**: The registration page.
- **products.html**: Displays a list of products available for purchase.
- **cart.html**: Displays the user's cart with products.
- **checkout.html**: Displays the checkout page where users confirm their orders.
- **orders.html**: Admin-only page to view all orders.

## Routes
The application has several routes defined for different functionalities:
- `/`: Home page (landing page).
- `/login`: Login page.
- `/logout`: Logout action.
- `/register`: Registration page.
- `/products`: Displays all products.
- `/cart`: Displays the user's shopping cart.
- `/cart/add`: Add product to cart.
- `/cart/remove`: Remove product from cart.
- `/cart/update`: Update cart item quantity.
- `/checkout`: Checkout page to confirm the order.
- `/orders`: Admin-only page to view orders.
- `/order/confirm`: Confirm order and process the payment.

## Dependencies
This project uses the following dependencies:
- Flask: Web framework.
- Flask-PyMongo: Flask extension for working with MongoDB.
- bcrypt: Password hashing and verification.
- Python-dotenv: Loads environment variables from a .env file.
- datetime: For handling dates and times in the project.
- bson: For working with BSON objects in MongoDB.

## Environment Variables
Make sure to configure the following environment variables:
- `MONGO_URI`: The connection URI for your MongoDB instance.
- `admins`: A comma-separated list of admin email addresses.

Example .env file:
```ini
MONGO_URI=mongodb://localhost:27017/khalidstoreshift
admins="admin@example.com,superadmin@example.com"


## Contributing
If you would like to contribute to the project, feel free to fork the repository, make changes, and submit a pull request. Please ensure your code follows the existing style and includes appropriate tests.

## License

soon ...