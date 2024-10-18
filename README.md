## Telegram Bot for Product Ordering
This Telegram bot allows users to register, login, and place orders for products. Users can select from available products, specify quantities, and confirm orders, which are then stored in a MySQL database.

## Features
- User Registration: New users can register by providing their name, mobile number, email, address, and city.
- User Login: Registered users can log in using their mobile number.
- Product Selection: Users can choose from a list of products (e.g., Milk, Butter, Dahi, Bread, Cheese) and specify quantities.
- Order Confirmation: Users can confirm their selections, and the order is stored in the database.
- Exit Option: Users can exit the bot at any time

## Technologies Used
- Python: Programming language used for bot development.
- Python-Telegram-Bot: Library for interacting with Telegram's Bot API.
- MySQL: Database used for storing user data and order details.

## Setup Instructions
###  Prerequisites
1. Python 3.x: Install Python from the official website.
2. MySQL: Install MySQL from the official website.
3. Python Packages: Install the necessary Python packages:
```
pip install mysql-connector-python python-telegram-bot
```
