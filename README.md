# 🏦 Smart Bank Management System | Python & MySQL

## 📌 Project Overview

The **Smart Bank Management System** is a desktop-based application developed as part of my MCA Semester 2 Mini Project. The project aims to simplify basic banking operations through a graphical user interface built using Python Tkinter and a MySQL database.

The application allows users to register, log in, manage account information, perform deposit and withdrawal transactions, view transaction history, and convert INR into selected foreign currencies.

This project helped me gain practical experience in Python programming, database connectivity, SQL queries, data management, and developing a user-friendly desktop application.

## 🎯 Project Objectives

- To develop a simple and user-friendly banking application.
- To manage customer registration and login.
- To maintain account information using MySQL.
- To perform basic deposit and withdrawal operations.
- To maintain and retrieve transaction records.
- To provide currency conversion functionality.
- To enable transaction history filtering and CSV export.

## 🛠️ Technologies Used

| Technology | Purpose |

| Python | Application development |
| Tkinter | Graphical User Interface (GUI) |
| MySQL | Database management |
| MySQL Connector | Python-MySQL connectivity |
| SQL | Data storage and retrieval |
| CSV | Transaction data export |

## ✨ Key Features

### 1. User Registration & Login
- New user registration.
- User authentication using username and password.
- Password reset functionality.

### 2. Account Management
- View customer account information.
- Update account details.
- Manage account type and address information.

### 3. Transaction Management
- Deposit money into an account.
- Withdraw money from an account.
- Update account balance after transactions.
- Validate transaction amounts and available balance.

### 4. Transaction History
- View previous transaction records.
- Filter transactions using date ranges.
- Filter by transaction type (Deposit or Withdrawal).
- Export transaction records into CSV format.

### 5. Currency Converter
- Enter an amount in INR.
- Select a target currency (USD, EUR, GBP, AUD, JPY).
- Retrieve conversion rates from the MySQL database.
- Display the converted amount.

## 🗄️ Database Management

The application uses MySQL to store and manage banking-related information.

The project references the following database tables:

- `users` – Customer registration and personal information.
- `accounts` – Account details, account type and balance.
- `transactions` – Deposit and withdrawal transaction records.
- `transaction_history` – Transaction descriptions and timestamps.
- `currency_rates` – Currency conversion rates.
- `branches` – Branch-related information.

## 📂 Project Structure

Smart-Bank-Management-System/
│
├── MainSmart_bank.py
├── db_config.py
├── user_auth.py
├── register_user.py
├── account_management.py
├── transaction_management.py
├── transactions.py
├── transaction_history.py
├── currency_converter.py
├── Mysqlconnectorbankapp.py
│
├── Smart_bank Management SystemOutPut_Screens.pdf
│
└── README.md

## 📚 Learning Outcomes

Through this project, I gained practical experience in:

- Developing desktop applications using Python Tkinter.
- Connecting Python applications with MySQL.
- Writing SQL queries for database operations.
- Performing CRUD operations.
- Managing transaction records and customer information.
- Filtering and exporting data into CSV format.
- Understanding the importance of data validation and application security.

## 🚀 Future Enhancements

- Improve password security and account recovery mechanisms.
- Add transaction-level balance tracking.
- Introduce enhanced reporting and data visualization.
- Improve the user interface and application responsiveness.
- Explore cloud-based database hosting and deployment.

## 👩‍💻 Project Information

**Project:** Smart Bank Management System  
**Academic Level:** MCA Semester 2 Mini Project  
**Programming Language:** Python  
**Database:** MySQL  
**Application Type:** Desktop Application

Developed as an academic project to gain practical knowledge of Python application development and database management.
