#Transaction_management
# transaction_management.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db_config import mysql


def show_transaction_management(app):
    app.clear_screen()
    tk.Label(app.root, text="💳 Transaction Management", font=("Helvetica", 16, "bold")).pack(pady=15)

    tk.Label(app.root, text="Amount to Deposit", font=("Helvetica", 12)).pack(pady=5)
    deposit_entry = tk.Entry(app.root, font=("Helvetica", 12))
    deposit_entry.pack(pady=5)

    tk.Label(app.root, text="Amount to Withdraw", font=("Helvetica", 12)).pack(pady=5)
    withdraw_entry = tk.Entry(app.root, font=("Helvetica", 12))
    withdraw_entry.pack(pady=5)

    def perform_deposit():
        amount = deposit_entry.get()
        if not amount or not amount.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid deposit amount.")
            return
        update_balance(app.logged_in_user, float(amount), "Deposit")

    def perform_withdraw():
        amount = withdraw_entry.get()
        if not amount or not amount.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid withdrawal amount.")
            return
        update_balance(app.logged_in_user, float(amount), "Withdrawal")

    def update_balance(username, amount, transaction_type):
        conn = mysql()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "User not found.")
                return

            user_id = user[0]

            cursor.execute("SELECT account_id, balance FROM accounts WHERE user_id = %s", (user_id,))
            account = cursor.fetchone()
            if not account:
                messagebox.showerror("Error", "Account not found.")
                return

            account_id, current_balance = account

            if transaction_type == "Deposit":
                new_balance = current_balance + amount
            elif transaction_type == "Withdrawal":
                if current_balance < amount:
                    messagebox.showwarning("Insufficient Balance", "Cannot withdraw more than current balance.")
                    return
                new_balance = current_balance - amount
            else:
                return

            # Update balance
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
            # Insert into transactions table
            cursor.execute(
                "INSERT INTO transactions (account_id, transaction_type, amount, date) VALUES (%s, %s, %s, NOW())",
                (account_id, transaction_type, amount))
            # Insert into transaction_history table
            description = f"{transaction_type} of ₹{amount}"
            cursor.execute("INSERT INTO transaction_history (account_id, description, date) VALUES (%s, %s, NOW())",
                           (account_id, description))

            conn.commit()
            messagebox.showinfo("Success", f"{transaction_type} of ₹{amount} successful.")

            # Refresh Account Management module if needed
            app.account_data_updated = True

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    # Buttons
    button_frame = tk.Frame(app.root)
    button_frame.pack(pady=15)

    tk.Button(button_frame, text="Deposit", command=perform_deposit, font=("Helvetica", 12), width=12,
              bg="lightgreen").grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Withdraw", command=perform_withdraw, font=("Helvetica", 12), width=12,
              bg="lightblue").grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Back", command=app.dashboard, font=("Helvetica", 12), width=12, bg="lightgrey").grid(
        row=0, column=2, padx=10)
