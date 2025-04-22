# transactions.py
import mysql.connector
from tkinter import messagebox


def perform_transaction(username, amount, txn_type):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Learn@02mysql",
            database="smart_bank"
        )
        cursor = conn.cursor()


def deposit(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount, date) VALUES (%s, 'Deposit', %s, %s)",
        (account_id, amount, datetime.now()))
    cursor.execute("INSERT INTO transaction_history (account_id, description, date) VALUES (%s, %s, %s)",
                   (account_id, f'Deposited ₹{amount}', datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()


def withdraw(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, date) VALUES (%s, 'Withdrawal', %s, %s)",
            (account_id, amount, datetime.now()))
        cursor.execute("INSERT INTO transaction_history (account_id, description, date) VALUES (%s, %s, %s)",
                       (account_id, f'Withdrew ₹{amount}', datetime.now()))
        conn.commit()
    else:
        raise Exception("Insufficient balance")

    cursor.close()
    conn.close()


def transfer_funds(from_account_id, to_account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,))
    from_balance = cursor.fetchone()[0]

    if from_balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, from_account_id))
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, to_account_id))

        now = datetime.now()
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, date) VALUES (%s, 'Withdrawal', %s, %s)",
            (from_account_id, amount, now))
        cursor.execute("INSERT INTO transaction_history (account_id, description, date) VALUES (%s, %s, %s)",
                       (from_account_id, f'Transferred ₹{amount} to account {to_account_id}', now))

        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, date) VALUES (%s, 'Deposit', %s, %s)",
            (to_account_id, amount, now))
        cursor.execute("INSERT INTO transaction_history (account_id, description, date) VALUES (%s, %s, %s)",
                       (to_account_id, f'Received ₹{amount} from account {from_account_id}', now))

        conn.commit()
    else:
        raise Exception("Insufficient balance for transfer")

    cursor.close()
    conn.close()

