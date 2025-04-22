# main.py
import tkinter as tk
from tkinter import messagebox
from user_auth import login_user, register_user, reset_user_password
import mysql.connector
import requests
def log_login_history(username):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Learn@02mysql",  # Add your MySQL password if any
            database="smart_bank"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            cursor.execute("INSERT INTO login_history (user_id) VALUES (%s)", (user_id,))
            conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("❌ Error logging login history:", err)


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

        if login_user(username, password):
            log_login_history(username)  # Logs the login attempt to the database
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
        tk.Label(self.root, text="🏦 Welcome to Smart Bank Dashboard", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        tk.Button(self.root, text="👤 Account Management", font=("Helvetica", 13), width=25, command=self.account_management).pack(pady=10)
        tk.Button(self.root, text="💰 Transactions", font=("Helvetica", 13), width=25, command=self.transaction_management).pack(pady=10)
        tk.Button(self.root, text="📜 Transaction History", font=("Helvetica", 13), width=25, command=self.transaction_history).pack(pady=10)
        tk.Button(self.root, text="🌐 Currency Converter", font=("Helvetica", 13), width=25, command=self.currency_converter).pack(pady=10)
        tk.Button(self.root, text="🚪 Logout", font=("Helvetica", 13), width=25, command=self.show_main_menu).pack(pady=20)


class SmartBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Bank Management System")
        self.root.geometry("600x500")
        self.root.config(bg="#f0f4f7")

        # Dummy account data for now (should come from a database)
        self.account_details = {
            'Account Number': '1234567890',
            'Account Type': 'Savings',
            'Balance': '10000 USD'
        }

        self.transaction_history = [
            {"date": "2025-04-10", "amount": "500 USD", "type": "Deposit", "status": "Successful"},
            {"date": "2025-04-12", "amount": "100 USD", "type": "Withdraw", "status": "Successful"}
        ]

        self.main_menu()

    def clear_screen(self):
        # This function clears the current screen before showing new content
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()

        # Main menu UI elements
        tk.Label(self.root, text="Welcome to Smart Bank", font=("Helvetica", 24, "bold"), bg="#f0f4f7").pack(pady=20)

        # Buttons for each feature
        tk.Button(self.root, text="Account Management", font=("Helvetica", 14), command=self.account_management).pack(
            pady=10)
        tk.Button(self.root, text="Transaction Management", font=("Helvetica", 14),
                  command=self.transaction_management).pack(pady=10)
        tk.Button(self.root, text="Transaction History", font=("Helvetica", 14),
                  command=self.transaction_history_display).pack(pady=10)
        tk.Button(self.root, text="Currency Converter", font=("Helvetica", 14), command=self.currency_converter).pack(
            pady=10)

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
            tk.Label(account_frame, text=value, font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1, column=1, padx=10,
                                                                                           pady=5)

        # Buttons to Update or Delete account
        tk.Button(self.root, text="Update Account", font=("Helvetica", 14), command=self.update_account).pack(pady=10)
        tk.Button(self.root, text="Delete Account", font=("Helvetica", 14), command=self.delete_account).pack(pady=10)

    def update_account(self):
        messagebox.showinfo("Coming Soon", "Account update functionality is under development.")

    def delete_account(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
        if confirm:
            messagebox.showinfo("Success", "Account deleted successfully!")
            self.main_menu()

    # Transaction Management: Deposit and Withdraw
    def transaction_management(self):
        self.clear_screen()

        tk.Label(self.root, text="💸 Transaction Management", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        transaction_frame = tk.Frame(self.root, bg="#f0f4f7")
        transaction_frame.pack()

        tk.Label(transaction_frame, text="Amount:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10,
                                                                                               pady=10)
        self.transaction_amount = tk.Entry(transaction_frame, font=("Helvetica", 12), width=20)
        self.transaction_amount.grid(row=0, column=1, padx=10, pady=10)

        self.transaction_type = tk.StringVar(value="Deposit")

        tk.Radiobutton(transaction_frame, text="Deposit", variable=self.transaction_type, value="Deposit",
                       font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        tk.Radiobutton(transaction_frame, text="Withdraw", variable=self.transaction_type, value="Withdraw",
                       font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=1, sticky="w", padx=20, pady=10)

        tk.Button(self.root, text="Submit Transaction", font=("Helvetica", 14), command=self.process_transaction).pack(
            pady=20)

    def process_transaction(self):
        amount = self.transaction_amount.get()
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        amount = float(amount)
        transaction_type = self.transaction_type.get()

        # Here you can add logic for transaction (deposit/withdraw)
        messagebox.showinfo("Transaction Successful", f"{transaction_type} of {amount} completed successfully!")

    # Transaction History: Display transaction history
    def transaction_history_display(self):
        self.clear_screen()

        tk.Label(self.root, text="📜 Transaction History", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        history_frame = tk.Frame(self.root, bg="#f0f4f7")
        history_frame.pack()

        for i, transaction in enumerate(self.transaction_history):
            tk.Label(history_frame, text=transaction['date'], font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1,
                                                                                                         column=0,
                                                                                                         padx=10,
                                                                                                         pady=5)
            tk.Label(history_frame, text=transaction['amount'], font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1,
                                                                                                           column=1,
                                                                                                           padx=10,
                                                                                                           pady=5)
            tk.Label(history_frame, text=transaction['type'], font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1,
                                                                                                         column=2,
                                                                                                         padx=10,
                                                                                                         pady=5)
            tk.Label(history_frame, text=transaction['status'], font=("Helvetica", 12), bg="#f0f4f7").grid(row=i + 1,
                                                                                                           column=3,
                                                                                                           padx=10,
                                                                                                           pady=5)

    # Currency Converter: Convert between currencies
    def currency_converter(self):
        self.clear_screen()

        tk.Label(self.root, text="🌐 Currency Converter", font=("Helvetica", 18, "bold"), bg="#f0f4f7").pack(pady=30)

        conversion_frame = tk.Frame(self.root, bg="#f0f4f7")
        conversion_frame.pack()

        tk.Label(conversion_frame, text="Amount:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10,
                                                                                              pady=10)
        self.amount_entry = tk.Entry(conversion_frame, font=("Helvetica", 12), width=20)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Convert", font=("Helvetica", 14), command=self.convert_currency).pack(pady=20)

    def convert_currency(self):
        amount = self.amount_entry.get()
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        amount = float(amount)

        # Fetch exchange rate from API (e.g., for USD to INR)
        exchange_rate = self.get_exchange_rate()

        if exchange_rate:
            converted_amount = amount * exchange_rate
            messagebox.showinfo("Conversion Result", f"{amount} USD = {converted_amount} INR")
        else:
            messagebox.showerror("Error", "Failed to fetch exchange rate. Please try again later.")

    def get_exchange_rate(self):
        # Example of using a currency conversion API (e.g., 'https://api.exchangerate-api.com')
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            return data["rates"].get("INR")
        except requests.exceptions.RequestException:
            return None


# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBankApp(root)
    root.mainloop()
