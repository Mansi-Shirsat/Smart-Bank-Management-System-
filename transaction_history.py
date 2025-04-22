#transaction history
import tkinter as tk
from tkinter import messagebox
import mysql.connector

class TransactionHistory:
    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

    def show_transaction_history(self):
        # Clear any existing widgets
        self.clear_screen()

        # Back Button to return to Dashboard
        tk.Button(self.root, text="Back to Dashboard", font=("Helvetica", 13), width=25,
                  command=self.back_to_dashboard).pack(pady=10)

        # Fetch transaction data from the database
        cursor = self.db.cursor()
        query = """SELECT t.transaction_id, t.amount, t.transaction_type, t.date, a.account_id 
                   FROM transactions t 
                   JOIN accounts a ON t.account_id = a.account_id 
                   WHERE a.user_id = %s ORDER BY t.date DESC"""
        cursor.execute(query, (self.user_id,))
        transactions = cursor.fetchall()

        if transactions:
            # Display the transaction history in a scrollable listbox or labels
            tk.Label(self.root, text="📜 Transaction History", font=("Helvetica", 18, "bold")).pack(pady=20)

            # Create a frame for scrollable content
            frame = tk.Frame(self.root)
            frame.pack(pady=10)

            canvas = tk.Canvas(frame)
            scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scroll_y.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.configure(yscrollcommand=scroll_y.set)

            transaction_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=transaction_frame, anchor="nw")

            # Iterate over the transactions and display them
            for transaction in transactions:
                transaction_id, amount, transaction_type, date, account_id = transaction
                transaction_text = f"Transaction ID: {transaction_id} | Account ID: {account_id} | Type: {transaction_type} | Amount: {amount} | Date: {date}"
                tk.Label(transaction_frame, text=transaction_text, font=("Helvetica", 10)).pack(pady=5)

            transaction_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            tk.Label(self.root, text="No transaction history found.", font=("Helvetica", 13)).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def back_to_dashboard(self):
        # Assuming `self.dashboard` is the method that shows the main dashboard screen
        from main import SmartBankApp  # Import the main class here to use the dashboard method
        app = SmartBankApp(self.root, self.db)
        app.dashboard()

