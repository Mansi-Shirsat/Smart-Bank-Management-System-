# main.py
import tkinter as tk
from tkinter import messagebox
from user_auth import login_user, register_user, reset_user_password
import mysql.connector


class SmartBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Smart Bank Management System")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f4f7")
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()
        title = tk.Label(self.root, text="Smart Bank Management System", font=("Helvetica", 20, "bold"), bg="#f0f4f7")
        title.pack(pady=40)

        btn_login = tk.Button(self.root, text="🔐 Login", font=("Helvetica", 14), width=20, command=self.login_screen)
        btn_register = tk.Button(self.root, text="📝 Register", font=("Helvetica", 14), width=20,
                                 command=self.register_screen)
        btn_exit = tk.Button(self.root, text="❌ Exit", font=("Helvetica", 14), width=20, command=self.root.destroy)

        btn_login.pack(pady=15)
        btn_register.pack(pady=15)
        btn_exit.pack(pady=15)

    def register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="📝 User Registration", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=20)
        form_frame = tk.Frame(self.root, bg="#f0f4f7")
        form_frame.pack()

        labels = [
            "Username", "Password", "Confirm Password", "Full Name", "Gender", "DOB (YYYY-MM-DD)",
            "Phone", "Address", "PAN", "Account Type", "Initial Deposit"
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Helvetica", 12), bg="#f0f4f7").grid(row=i, column=0,
                                                                                              sticky="e", pady=5,
                                                                                              padx=5)
            entry = tk.Entry(form_frame, width=30, show="*" if "Password" in label else "")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label] = entry

        btn_register = tk.Button(self.root, text="Register", font=("Helvetica", 14), command=self.handle_register)
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.show_main_menu)
        btn_register.pack(pady=10)
        btn_back.pack()

    def handle_register(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        user_data = {
            "username": data["Username"],
            "password": data["Password"],
            "confirm_password": data["Confirm Password"],
            "full_name": data["Full Name"],
            "Gender": data["gender"],  # Assuming 'gender' is the key in the data dictionary
            "dob": data["DOB (YYYY-MM-DD)"],
            "phone": data["Phone"],
            "address": data["Address"],
            "pan": data["PAN"],
            "account_type": data["Account Type"],
            "deposit": data["Initial Deposit"]
        }

        if register_user(user_data):
            messagebox.showinfo("Success", "✅ User registered successfully!")
            self.login_screen()
        else:
            messagebox.showerror("Error", "❌ Registration failed!")

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="🔐 User Login", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        login_frame = tk.Frame(self.root, bg="#f0f4f7")
        login_frame.pack()

        tk.Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10,
                                                                                           pady=10)
        self.login_username_entry = tk.Entry(login_frame, width=30)
        self.login_username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10,
                                                                                           pady=10)
        self.login_password_entry = tk.Entry(login_frame, show="*", width=30)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_login = tk.Button(self.root, text="Login", font=("Helvetica", 14), command=self.handle_login)
        btn_forgot = tk.Button(self.root, text="🔑 Forgot Password?", font=("Helvetica", 10),
                               command=self.forgot_password_screen, fg="blue", bg="#f0f4f7", relief="flat")
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.show_main_menu)

        btn_login.pack(pady=10)
        btn_forgot.pack()
        btn_back.pack()

    def handle_login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if login_user(username, password):
            messagebox.showinfo("Success", "✅ Login successful!")
            self.dashboard()
        else:
            messagebox.showerror("Error", "❌ Invalid credentials!")

    def forgot_password_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🔐 Reset Password", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack()

        labels = ["Username", "Phone", "PAN", "New Password", "Confirm Password"]
        self.reset_entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label + ":", font=("Helvetica", 12), bg="#f0f4f7").grid(row=i, column=0, sticky="e",
                                                                                         pady=5, padx=5)
            entry = tk.Entry(frame, width=30, show="*" if "Password" in label else "")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.reset_entries[label] = entry

        btn_reset = tk.Button(self.root, text="Reset Password", font=("Helvetica", 13),
                              command=self.handle_password_reset)
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.login_screen)

        btn_reset.pack(pady=10)
        btn_back.pack()

    def handle_password_reset(self):
        data = {key: entry.get() for key, entry in self.reset_entries.items()}

        if data["New Password"] != data["Confirm Password"]:
            messagebox.showerror("Error", "❌ Passwords do not match!")
            return

        if reset_user_password(data["Username"], data["Phone"], data["PAN"], data["New Password"]):
            messagebox.showinfo("Success", "✅ Password reset successful!")
            self.login_screen()
        else:
            messagebox.showerror("Error", "❌ Failed to reset password. Please check your details.")

    def dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="🏦 Welcome to Smart Bank Dashboard", font=("Helvetica", 18, "bold"),
                 bg="#f0f4f7").pack(pady=30)

        tk.Button(self.root, text="👤 Account Management", font=("Helvetica", 13), width=25,
                  command=self.account_management).pack(pady=10)
        tk.Button(self.root, text="💰 Transactions", font=("Helvetica", 13), width=25,
                  command=self.transaction_management).pack(pady=10)
        tk.Button(self.root, text="📜 Transaction History", font=("Helvetica", 13), width=25,
                  command=self.transaction_history).pack(pady=10)
        tk.Button(self.root, text="🌐 Currency Converter", font=("Helvetica", 13), width=25,
                  command=self.currency_converter).pack(pady=10)
        tk.Button(self.root, text="🚪 Logout", font=("Helvetica", 13), width=25, command=self.show_main_menu).pack(
            pady=20)

    # Account_management
    def account_management(self):
        # Account Management: View, Update, and Delete Account
        def account_management(self):
            self.clear_screen()
            tk.Label(self.root, text="📝 Account Management", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

            # Display account details
            account_frame = tk.Frame(self.root, bg="#f0f4f7")
            account_frame.pack()

            for i, (key, value) in enumerate(self.account_details.items()):
                tk.Label(account_frame, text=f"{key}:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1, column=0,
                                                                                                   sticky="e", padx=10,
                                                                                                   pady=5)
                tk.Label(account_frame, text=value, font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1, column=1,
                                                                                               padx=10,
                                                                                               pady=5)

            # Buttons to Update or Delete account
            tk.Button(self.root, text="Update Account", font=("Helvetica", 14), command=self.update_account).pack(
                pady=10)
            tk.Button(self.root, text="Delete Account", font=("Helvetica", 14), command=self.delete_account).pack(
                pady=10)

        def update_account(self):
            messagebox.showinfo("Coming Soon", "Account update functionality is under development.")

        def delete_account(self):
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
            if confirm:
                messagebox.showinfo("Success", "Account deleted successfully!")
                self.main_menu()
    def account_management(self):
        self.clear_screen()
        tk.Label(self.root, text="👤 Account Management", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=20)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack()

        # Fetch user account info from database
        conn = mysql.connector.connect(host="localhost", user="root", password="Learn@02mysql", database="smart_bank")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (self.login_username_entry.get(),))
        account = cursor.fetchone()

        if not account:
            messagebox.showerror("Error", "❌ Account not found!")
            self.dashboard()
            return

        # Labels and fields
        tk.Label(frame, text="Full Name:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5,
                                                                                      sticky="e")
        tk.Label(frame, text=account['full_name'], bg="#f0f4f7", font=("Helvetica", 12)).grid(row=0, column=1, padx=10,
                                                                                              pady=5, sticky="w")

        tk.Label(frame, text="Account Type:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=1, column=0, padx=10,
                                                                                         pady=5, sticky="e")
        self.account_type_var = tk.StringVar(value=account['account_type'])
        tk.Radiobutton(frame, text="Recurring", variable=self.account_type_var, value="Recurring", bg="#f0f4f7",
                       font=("Helvetica", 12)).grid(row=1, column=1, sticky="w")
        tk.Radiobutton(frame, text="Salary", variable=self.account_type_var, value="Salary", bg="#f0f4f7",
                       font=("Helvetica", 12)).grid(row=1, column=2, sticky="w")

        # Branch dropdown
        tk.Label(frame, text="Branch:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5,
                                                                                   sticky="e")
        cursor.execute("SELECT branch_name FROM branches")
        branches = [row['branch_name'] for row in cursor.fetchall()]
        self.branch_var = tk.StringVar(value=account['branch'])
        branch_dropdown = tk.OptionMenu(frame, self.branch_var, *branches)
        branch_dropdown.config(font=("Helvetica", 12))
        branch_dropdown.grid(row=2, column=1, pady=5, sticky="w")

        # Update button
        tk.Button(self.root, text="Update Account", font=("Helvetica", 13), command=self.update_account_info).pack(
            pady=10)
        tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=5)

        conn.close()

    # Transaction_management
    def transaction_management(self):
        self.clear_screen()
        tk.Label(self.root, text="💰 Transaction Management", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        # Frame for transaction options
        transaction_frame = tk.Frame(self.root, bg="#f0f4f7")
        transaction_frame.pack()

        # Entry fields for transaction details
        tk.Label(transaction_frame, text="Amount to Deposit:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          pady=10)
        self.deposit_amount_entry = tk.Entry(transaction_frame, width=30)
        self.deposit_amount_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(transaction_frame, text="Amount to Withdraw:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=10)
        self.withdraw_amount_entry = tk.Entry(transaction_frame, width=30)
        self.withdraw_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Transaction buttons
        tk.Button(self.root, text="Deposit", font=("Helvetica", 14), command=self.handle_deposit).pack(pady=10)
        tk.Button(self.root, text="Withdraw", font=("Helvetica", 14), command=self.handle_withdraw).pack(pady=10)
        tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=10)

    def handle_deposit(self):
        amount = self.deposit_amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "❌ Please enter a valid deposit amount.")
            return

        # Insert deposit transaction into the database here
        messagebox.showinfo("Success", f"✅ ${amount} deposited successfully!")

    def handle_withdraw(self):
        amount = self.withdraw_amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "❌ Please enter a valid withdrawal amount.")
            return

        # Check if withdrawal is possible (e.g., balance check) here

        messagebox.showinfo("Success", f"✅ ${amount} withdrawn successfully!")

    # Transaction_history
    def transaction_history(self):
        self.clear_screen()
        tk.Label(self.root, text="📜 Transaction History", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        # Transaction History Table (Example: displaying static data or from DB)
        transaction_history_frame = tk.Frame(self.root, bg="#f0f4f7")
        transaction_history_frame.pack()

        # Sample data
        transactions = [("2025-04-01", "Deposit", "$500"), ("2025-04-02", "Withdraw", "$200")]

        for i, transaction in enumerate(transactions):
            tk.Label(transaction_history_frame, text=f"Date: {transaction[0]}", font=("Helvetica", 12),
                     bg="#f0f4f7").grid(row=i, column=0, padx=10, pady=5)
            tk.Label(transaction_history_frame, text=f"Type: {transaction[1]}", font=("Helvetica", 12),
                     bg="#f0f4f7").grid(row=i, column=1, padx=10, pady=5)
            tk.Label(transaction_history_frame, text=f"Amount: {transaction[2]}", font=("Helvetica", 12),
                     bg="#f0f4f7").grid(row=i, column=2, padx=10, pady=5)

        tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=10)

    # Currenct_converter
    def currency_converter(self):
        self.clear_screen()
        tk.Label(self.root, text="🌐 Currency Converter", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        # Conversion form frame
        converter_frame = tk.Frame(self.root, bg="#f0f4f7")
        converter_frame.pack()

        tk.Label(converter_frame, text="Amount in INR:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0,
                                                                                                    padx=10, pady=10)
        self.inr_amount_entry = tk.Entry(converter_frame, width=30)
        self.inr_amount_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(converter_frame, text="Convert to Currency:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          pady=10)
        self.currency_type_entry = tk.Entry(converter_frame, width=30)
        self.currency_type_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Convert", font=("Helvetica", 14), command=self.handle_currency_conversion).pack(
            pady=10)
        tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=10)

    def handle_currency_conversion(self):
        inr_amount = self.inr_amount_entry.get()
        currency_type = self.currency_type_entry.get()

        if not inr_amount.isdigit() or int(inr_amount) <= 0:
            messagebox.showerror("Error", "❌ Please enter a valid amount in INR.")
            return

        # Retrieve conversion rate from the currency_rates table and perform conversion
        # Assuming the rate is 75 INR to 1 USD as an example (replace with DB query)
        conversion_rate = 75
        converted_amount = int(inr_amount) / conversion_rate

        messagebox.showinfo("Converted Amount", f"✅ {inr_amount} INR = {converted_amount:.2f} {currency_type.upper()}")


# Start the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBankApp(root)
    root.mainloop()
##########################################################################################################################
#main.py
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk

import datetime
import mysql.connector
import csv
from db_config import get_connection
from user_auth import login_user, register_user, reset_user_password
from currency_converter import get_conversion_rate
from datetime import datetime


# ✅ MySQL Database Connection Function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Learn@02mysql",
        database="smart_bank"
    )


class SmartBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Smart Bank Management System")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f4f7")
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()
        title = tk.Label(self.root, text="Smart Bank Management System", font=("Helvetica", 20, "bold"), bg="#f0f4f7")
        title.pack(pady=40)

        btn_login = tk.Button(self.root, text="🔐 Login", font=("Helvetica", 14), width=20, command=self.login_screen)
        btn_register = tk.Button(self.root, text="📝 Register", font=("Helvetica", 14), width=20, command=self.register_screen)
        btn_exit = tk.Button(self.root, text="❌ Exit", font=("Helvetica", 14), width=20, command=self.root.destroy)

        btn_login.pack(pady=15)
        btn_register.pack(pady=15)
        btn_exit.pack(pady=15)

    def register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="📝 User Registration", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=20)
        form_frame = tk.Frame(self.root, bg="#f0f4f7")
        form_frame.pack()

        labels = [
            "Username", "Password", "Confirm Password", "Full Name","Gender", "DOB (YYYY-MM-DD)",
            "Phone", "Address", "PAN", "Account Type", "Initial Deposit"
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Helvetica", 12), bg="#f0f4f7").grid(row=i, column=0, sticky="e", pady=5, padx=5)
            entry = tk.Entry(form_frame, width=30, show="*" if "Password" in label else "")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label] = entry

        btn_register = tk.Button(self.root, text="Register", font=("Helvetica", 14), command=self.handle_register)
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.show_main_menu)
        btn_register.pack(pady=10)
        btn_back.pack()

    def handle_register(self):
        data = {key: entry.get() for key, entry in self.entries.items()}

        # Validate and convert DOB to the correct format (YYYY-MM-DD)
        try:
            dob = datetime.strptime(data["DOB (YYYY-MM-DD)"], "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "❌ Invalid date format. Please use YYYY-MM-DD format.")
            return

        # Ensure the gender value is fetched from the radio buttons
        gender = self.gender_var.get()

        # Prepare user data dictionary
        user_data = {
            "username": data["Username"],
            "password": data["Password"],
            "confirm_password": data["Confirm Password"],
            "full_name": data["Full Name"],
            "gender": gender,
            "dob": dob,
            "phone": data["Phone"],
            "address": data["Address"],
            "pan": data["PAN"],
            "account_type": data["Account Type"],
            "deposit": data["Initial Deposit"]
        }


        # Call register_user from register_user.py
        if register_user(user_data):
            messagebox.showinfo("Success", "✅ User registered successfully!")
            self.login_screen()
        else:
            messagebox.showerror("Error", "❌ Registration failed!")

    # Example method where account type is updated (e.g., in response to a button click)
    def handle_update_account_type(self):
        new_account_type = self.account_type_var.get()  # Get the selected account type from input field
        self.update_account_type(new_account_type)

    def update_account_type(self, new_account_type):
        try:
            # Establish connection with the database
            conn = get_connection()
            cursor = conn.cursor()

            # Update query to change the account type in the accounts table
            update_query = """
                UPDATE accounts
                SET account_type = %s
                WHERE user_id = %s
            """
            # Execute the query with the new account type and the logged-in user ID
            cursor.execute(update_query,
                           (new_account_type, self.logged_in_user_id))  # Assuming logged_in_user_id exists
            conn.commit()

            messagebox.showinfo("Success", "✅ Account type updated successfully.")
            self.refresh_transaction_history()  # Refresh the transaction history after updating the account type

        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to update account type: {e}")
        finally:
            if conn:
                conn.close()

    def refresh_transaction_history(self):
        # Re-fetch the updated transaction history from the database
        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                   SELECT 
                       a.account_id,
                       u.full_name,
                       a.branch_name,
                       a.account_type,
                       th.description,
                       th.date
                   FROM transaction_history th
                   JOIN accounts a ON th.account_id = a.account_id
                   JOIN users u ON a.user_id = u.user_id
                   ORDER BY th.date DESC
               """
            cursor.execute(query)
            records = cursor.fetchall()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch transaction history:\n{e}")
            return

        finally:
            if connection:
                connection.close()

        # Update the TreeView with new transaction history
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in records:
            self.tree.insert("", "end", values=row)

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="🔐 User Login", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        login_frame = tk.Frame(self.root, bg="#f0f4f7")
        login_frame.pack()

        tk.Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=10)
        self.login_username_entry = tk.Entry(login_frame, width=30)
        self.login_username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=10)
        self.login_password_entry = tk.Entry(login_frame, show="*", width=30)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_login = tk.Button(self.root, text="Login", font=("Helvetica", 14), command=self.handle_login)
        btn_forgot = tk.Button(self.root, text="🔑 Forgot Password?", font=("Helvetica", 10), command=self.forgot_password_screen, fg="blue", bg="#f0f4f7", relief="flat")
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.show_main_menu)

        btn_login.pack(pady=10)
        btn_forgot.pack()
        btn_back.pack()

    def handle_login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if login_user(username, password):  # Check if login is successful
            # Establish a connection to the database to get the user_id
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # Set the logged_in_user_id to the retrieved user_id
                self.logged_in_user_id = result[0]
                messagebox.showinfo("Success", "✅ Login successful!")
                self.dashboard()  # Proceed to the dashboard
            else:
                messagebox.showerror("Error", "❌ User not found.")
        else:
            messagebox.showerror("Error", "❌ Invalid credentials!")
    def forgot_password_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🔐 Reset Password", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack()

        labels = ["Username", "Phone", "PAN", "New Password", "Confirm Password"]
        self.reset_entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label + ":", font=("Helvetica", 12), bg="#f0f4f7").grid(row=i, column=0, sticky="e", pady=5, padx=5)
            entry = tk.Entry(frame, width=30, show="*" if "Password" in label else "")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.reset_entries[label] = entry

        btn_reset = tk.Button(self.root, text="Reset Password", font=("Helvetica", 13), command=self.handle_password_reset)
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.login_screen)

        btn_reset.pack(pady=10)
        btn_back.pack()

    def handle_password_reset(self):
        data = {key: entry.get() for key, entry in self.reset_entries.items()}

        if data["New Password"] != data["Confirm Password"]:
            messagebox.showerror("Error", "❌ Passwords do not match!")
            return

        if reset_user_password(data["Username"], data["Phone"], data["PAN"], data["New Password"]):
            messagebox.showinfo("Success", "✅ Password reset successful!")
            self.login_screen()
        else:
            messagebox.showerror("Error", "❌ Failed to reset password. Please check your details.")

    def dashboard(self):
            self.clear_screen()
            tk.Label(self.root, text="🏦 Welcome to Smart Bank Dashboard", font=("Helvetica", 18, "bold"),
                     bg="#f0f4f7").pack(pady=30)

            tk.Button(self.root, text="👤 Account Management", font=("Helvetica", 13), width=25,
                      command=self.account_management).pack(pady=10)
            tk.Button(self.root, text="💰 Transactions", font=("Helvetica", 13), width=25,
                      command=self.show_transaction_management).pack(pady=10)
            tk.Button(self.root, text="📜 Transaction History", font=("Helvetica", 13), width=25,
                      command=self.show_transaction_history).pack(pady=10)

            tk.Button(self.root, text="🌐 Currency Converter", font=("Helvetica", 13), width=25,
                      command=self.currency_converter).pack(pady=10)
            tk.Button(self.root, text="🚪 Logout", font=("Helvetica", 13), width=25, command=self.show_main_menu).pack(
                pady=20)

    #Account_management

    def account_management(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import mysql.connector

        self.clear_screen()
        tk.Label(self.root, text="👤 Account Management", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=20)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(frame, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        username_entry.insert(0, self.login_username_entry.get())
        username_entry.config(state="disabled")

        details_text = tk.Text(self.root, height=15, width=70, font=("Helvetica", 10))
        details_text.pack(pady=10)
        details_text.config(state=tk.DISABLED)  # Make it read-only initially

        update_frame = tk.Frame(self.root, bg="#f0f4f7")
        update_frame.pack(pady=5)

        # Change Account Type
        tk.Label(update_frame, text="Change Account Type:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=0, column=0)
        acc_type_var = tk.StringVar()
        acc_type_combo = ttk.Combobox(update_frame, textvariable=acc_type_var, values=["Recurring", "Salary"], state="readonly")
        acc_type_combo.grid(row=0, column=1, padx=5)

        # Change Address
        tk.Label(update_frame, text="New Address:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=1, column=0)
        new_address_entry = tk.Entry(update_frame, width=30)
        new_address_entry.grid(row=1, column=1, padx=5)

        # Optional: Gender selection
        tk.Label(update_frame, text="Gender:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=2, column=0)
        gender_var = tk.StringVar()
        tk.Radiobutton(update_frame, text="Male", variable=gender_var, value="Male", bg="#f0f4f7").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(update_frame, text="Female", variable=gender_var, value="Female", bg="#f0f4f7").grid(row=2, column=1, padx=80, sticky="w")

        def fetch_details():
            username = username_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Please enter a username.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="Learn@02mysql", database="smart_bank"
                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.user_id, u.full_name, u.dob, u.gender, u.phone, u.address, u.pan, u.account_type, 
                           u.deposit, a.account_id, a.branch_name, a.balance
                    FROM users u
                    LEFT JOIN accounts a ON u.user_id = a.user_id
                    WHERE u.username = %s
                """, (username,))
                result = cursor.fetchone()
                conn.close()

                details_text.config(state=tk.NORMAL)
                details_text.delete("1.0", tk.END)

                if result:
                    for key, value in result.items():
                        details_text.insert(tk.END, f"{key.replace('_', ' ').title()}: {value}\n")
                    details_text.config(state=tk.DISABLED)

                    acc_type_var.set(result.get("account_type", ""))
                    new_address_entry.delete(0, tk.END)
                    new_address_entry.insert(0, result.get("address", ""))
                    gender_var.set(result.get("gender", ""))
                else:
                    messagebox.showerror("Not Found", "User not found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))

        def update_details():
            username = username_entry.get().strip()
            new_type = acc_type_var.get().strip()
            new_address = new_address_entry.get().strip()
            gender = gender_var.get().strip()

            if not username:
                messagebox.showerror("Error", "Enter a username first.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="Learn@02mysql", database="smart_bank"
                )
                cursor = conn.cursor()

                # Update account_type if provided
                if new_type:
                    cursor.execute("UPDATE users SET account_type=%s WHERE username=%s", (new_type, username))

                # Update gender if provided
                if gender:
                    cursor.execute("UPDATE users SET gender=%s WHERE username=%s", (gender, username))

                # Update address and also update branch based on address
                if new_address:
                    cursor.execute("UPDATE users SET address=%s WHERE username=%s", (new_address, username))
                    # Check if a branch exists at new address
                    cursor.execute("SELECT branch_name FROM branches WHERE address = %s", (new_address,))
                    branch_result = cursor.fetchone()
                    if branch_result:
                        branch_name = branch_result[0]
                        cursor.execute("""
                            UPDATE accounts 
                            SET branch_name = %s 
                            WHERE user_id = (SELECT user_id FROM users WHERE username = %s)
                        """, (branch_name, username))

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Account details updated.")
                fetch_details()
            except mysql.connector.Error as e:
                messagebox.showerror("Update Error", str(e))

        def delete_account():
            username = username_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Please enter a username.")
                return

            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this account?")
            if confirm:
                try:
                    conn = mysql.connector.connect(
                        host="localhost", user="root", password="Learn@02mysql", database="smart_bank"
                    )
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
                    cursor.execute("DELETE FROM accounts WHERE user_id = (SELECT user_id FROM users WHERE username = %s)", (username,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Account deleted successfully.")
                    self.show_main_menu()
                except mysql.connector.Error as e:
                    messagebox.showerror("Deletion Error", str(e))

        # Buttons
        tk.Button(self.root, text="Fetch Details", font=("Helvetica", 12), command=fetch_details).pack(pady=5)
        tk.Button(self.root, text="Update Details", font=("Helvetica", 12), command=update_details).pack(pady=5)
        tk.Button(self.root, text="Delete Account", font=("Helvetica", 12), command=delete_account).pack(pady=5)
        tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=10)

    #Transaction_management
    def show_transaction_management(self):
        self.clear_screen()
        tk.Label(self.root, text="💸 Transaction Management", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Amount Entry Fields
        tk.Label(self.root, text="Amount to Deposit:", font=("Helvetica", 12)).pack()
        deposit_entry = tk.Entry(self.root, font=("Helvetica", 12))
        deposit_entry.pack(pady=5)

        tk.Label(self.root, text="Amount to Withdraw:", font=("Helvetica", 12)).pack()
        withdraw_entry = tk.Entry(self.root, font=("Helvetica", 12))
        withdraw_entry.pack(pady=5)

        def get_account_id():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT account_id FROM accounts WHERE user_id = %s", (self.logged_in_user_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None

        def update_balance(account_id, new_balance):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
            conn.commit()
            conn.close()

        def log_transaction(account_id, transaction_type, amount):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (account_id, transaction_type, amount, date) VALUES (%s, %s, %s, NOW())",
                (account_id, transaction_type, amount))
            cursor.execute("INSERT INTO transaction_history (account_id, description, date) VALUES (%s, %s, NOW())",
                           (account_id, f"{transaction_type} of ₹{amount}",))
            conn.commit()
            conn.close()

        def deposit():
            try:
                amount = float(deposit_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                account_id = get_account_id()
                if account_id is None:
                    messagebox.showerror("Error", "Account not found.")
                    return

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
                current_balance = cursor.fetchone()[0]
                conn.close()

                new_balance = current_balance + amount
                update_balance(account_id, new_balance)
                log_transaction(account_id, "Deposit", amount)
                messagebox.showinfo("Success", f"₹{amount} deposited successfully!")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.")

        def withdraw():
            try:
                amount = float(withdraw_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                account_id = get_account_id()
                if account_id is None:
                    messagebox.showerror("Error", "Account not found.")
                    return

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
                current_balance = cursor.fetchone()[0]
                conn.close()

                if current_balance < amount:
                    messagebox.showerror("Error", "Insufficient balance.")
                    return

                new_balance = current_balance - amount
                update_balance(account_id, new_balance)
                log_transaction(account_id, "Withdrawal", amount)
                messagebox.showinfo("Success", f"₹{amount} withdrawn successfully!")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.")

        # Buttons
        tk.Button(self.root, text="Deposit", font=("Helvetica", 12), width=15, bg="lightgreen", command=deposit).pack(
            pady=10)
        tk.Button(self.root, text="Withdraw", font=("Helvetica", 12), width=15, bg="lightblue", command=withdraw).pack(
            pady=5)
        tk.Button(self.root, text="Back", font=("Helvetica", 12), width=15, bg="gray", command=self.dashboard).pack(
            pady=10)

        #Transaction_history

    def show_transaction_history(self):
        self.clear_screen()

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame, text="Transaction History", font=("Arial", 18, "bold")).pack(pady=10)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                   SELECT 
                       a.account_id,
                       u.full_name,
                       a.branch_name,
                       a.account_type,
                       th.description,
                       th.date
                   FROM transaction_history th
                   JOIN accounts a ON th.account_id = a.account_id
                   JOIN users u ON a.user_id = u.user_id
                   ORDER BY th.date DESC
               """
            cursor.execute(query)
            records = cursor.fetchall()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch transaction history:\n{e}")
            return

        finally:
            if connection:
                connection.close()
        filter_frame = tk.Frame(self.root, bg="#f0f4f7")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):", bg="#f0f4f7").grid(row=0, column=0, padx=5)
        start_entry = tk.Entry(filter_frame)
        start_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="End Date (YYYY-MM-DD):", bg="#f0f4f7").grid(row=0, column=2, padx=5)
        end_entry = tk.Entry(filter_frame)
        end_entry.grid(row=0, column=3, padx=5)

        def refresh_history():
            start_date = start_entry.get()
            end_date = end_entry.get()
            query = """
                SELECT a.account_id, u.full_name, a.branch_name, a.account_type, th.description, th.date
                FROM transaction_history th
                JOIN accounts a ON th.account_id = a.account_id
                JOIN users u ON a.user_id = u.user_id
                WHERE a.user_id = %s
            """
            params = [self.logged_in_user_id]
            if start_date:
                query += " AND th.date >= %s"
                params.append(start_date)
            if end_date:
                query += " AND th.date <= %s"
                params.append(end_date)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            records = cursor.fetchall()
            conn.close()

            for row in tree.get_children():
                tree.delete(row)
            for row in records:
                tree.insert("", "end", values=row)

        tk.Button(filter_frame, text="🔄 Filter & Refresh", command=refresh_history).grid(row=0, column=4, padx=10)

        # TreeView Table
        columns = ("Account ID", "Full Name", "Branch", "Account Type", "Description", "Date")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        # Clear previous rows if reloading
        for row in tree.get_children():
            tree.delete(row)

        # Insert latest rows
        for row in records:
            tree.insert("", "end", values=row)


        def export_to_csv():
            with open("transaction_history.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                for row_id in tree.get_children():
                    row = tree.item(row_id)['values']
                    writer.writerow(row)
            messagebox.showinfo("Export", "📁 Transaction history exported to 'transaction_history.csv'")

            # Buttons

        tk.Button(self.root, text="🔄 Refresh / Filter", font=("Helvetica", 12), command=refresh_history).pack(pady=5)
        tk.Button(self.root, text="⬇ Export to CSV", font=("Helvetica", 12), command=export_to_csv).pack(pady=5)
        tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=10)

        # Load data initially
        refresh_history()
       #currency_converter
    def currency_converter(self):
        self.clear_screen()

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame, text="Currency Converter", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(frame, text="Amount in INR:").pack(pady=5)
        inr_amount_entry = tk.Entry(frame)
        inr_amount_entry.pack(pady=5)

        tk.Label(frame, text="Convert to Currency:").pack(pady=5)
        currency_options = ["USD", "EUR", "GBP", "AUD", "JPY"]  # You can extend this list
        currency_dropdown = ttk.Combobox(frame, values=currency_options)
        currency_dropdown.pack(pady=5)

        def convert_currency():
            try:
                amount_in_inr = float(inr_amount_entry.get())
                selected_currency = currency_dropdown.get()
                if not selected_currency:
                    messagebox.showerror("Error", "Please select a currency.")
                    return

                rate = get_conversion_rate(selected_currency)
                if rate:
                    converted_amount = amount_in_inr * rate
                    messagebox.showinfo("Conversion Result",
                                        f"{amount_in_inr} INR = {converted_amount:.2f} {selected_currency}")
                else:
                    messagebox.showerror("Error", f"No rate found for INR to {selected_currency}.")

            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.")

        tk.Button(frame, text="Convert", command=convert_currency).pack(pady=10)
        tk.Button(frame, text="⬅ Back", font=("Helvetica", 12), command=self.dashboard).pack(pady=10)
# Start the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBankApp(root)
    root.mainloop()









