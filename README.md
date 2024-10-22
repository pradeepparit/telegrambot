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
### Database Setup
1. Create the Database:
- Open MySQL and create a new database for the bot:
```
CREATE DATABASE telegrambot;
```
2. Create Tables:
- Create tables for storing user data and order details.
-Example table structures:
```
CREATE TABLE users (
  ID INT AUTO_INCREMENT PRIMARY KEY,
  NAME VARCHAR(255),
  MOBILE_NO VARCHAR(20),
  EMAIL VARCHAR(255),
  ADDRESS VARCHAR(255),
  CITY VARCHAR(255),
  CHAT_ID VARCHAR(50)
);

CREATE TABLE order_list (
  ORDER_ID INT AUTO_INCREMENT PRIMARY KEY,
  USER_ID INT,
  PRODUCTS TEXT,
  TOTAL INT,
  FOREIGN KEY (USER_ID) REFERENCES users(ID)
);

```
