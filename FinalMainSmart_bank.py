#main.py
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk

import columns
import mysql.connector
import csv


from db_config import get_connection
from user_auth import login_user, register_user, reset_user_password
from currency_converter import get_conversion_rate


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
            "Username", "Password", "Confirm Password", "Full Name", "Gender", "DOB (YYYY-MM-DD)",
            "Phone", "Address", "PAN", "Account Type", "Initial Deposit"
        ]

        self.entries = {}

        # Loop through labels to create entries for each
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Helvetica", 12), bg="#f0f4f7").grid(row=i, column=0,
                                                                                              sticky="e", pady=5,
                                                                                              padx=5)

            if label == "Gender":
                # Create a dropdown for gender selection
                gender_options = ["Male", "Female", "Other"]
                self.gender_var = tk.StringVar(value=gender_options[0])  # Default value set to "Male"
                gender_menu = ttk.Combobox(form_frame, textvariable=self.gender_var, values=gender_options,
                                           state="readonly")
                gender_menu.grid(row=i, column=1, pady=5, padx=5)
            else:
                entry = tk.Entry(form_frame, width=30, show="*" if "Password" in label else "")
                entry.grid(row=i, column=1, pady=5, padx=5)
                self.entries[label] = entry

        btn_register = tk.Button(self.root, text="Register", font=("Helvetica", 14), command=self.handle_register)
        btn_back = tk.Button(self.root, text="⬅ Back", font=("Helvetica", 12), command=self.show_main_menu)
        btn_register.pack(pady=10)
        btn_back.pack()
#Handle_register
    def handle_register(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        gender = self.gender_var.get()  # Get the selected gender from dropdown

        user_data = {
            "username": data["Username"],
            "password": data["Password"],
            "confirm_password": data["Confirm Password"],
            "full_name": data["Full Name"],
            "gender": gender,  # Use the selected gender
            "dob": data["DOB (YYYY-MM-DD)"],
            "phone": data["Phone"],
            "address": data["Address"],
            "pan": data["PAN"],
            "account_type": data["Account Type"],
            "deposit": data["Initial Deposit"]
        }

        if register_user(user_data):
            # ✅ Insert into accounts after user is created
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT user_id FROM users WHERE username = %s", (user_data["username"],))
            user_id_result = cursor.fetchone()
            if user_id_result:
                user_id = user_id_result[0]
                cursor.execute("""
                    INSERT INTO accounts (user_id, account_type, balance, branch_name)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, user_data["account_type"], float(user_data["deposit"]), "Chinchwad"))

                # Log initial deposit to transaction history
                cursor.execute("""
                    INSERT INTO transaction_history (account_id, description, date)
                    VALUES ((SELECT account_id FROM accounts WHERE user_id = %s), %s, NOW())
                """, (user_id, f"Initial deposit of ₹{user_data['deposit']}"))

                conn.commit()
            conn.close()

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
            self.logged_in_username = username  # ✅ Define this for future access
            # Also store user_id for other operations
            # Check if login is successful
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

        tk.Label(frame, text="Enter Username:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10,
                                                                                           pady=5)
        username_entry = tk.Entry(frame, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        details_text = tk.Text(self.root, height=15, width=70, font=("Helvetica", 10))
        details_text.pack(pady=10)
        details_text.config(state=tk.DISABLED)  # Make it read-only initially

        update_frame = tk.Frame(self.root, bg="#f0f4f7")
        update_frame.pack(pady=5)

        # Change Account Type
        tk.Label(update_frame, text="Change Account Type:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=0, column=0)
        acc_type_var = tk.StringVar()
        acc_type_combo = ttk.Combobox(update_frame, textvariable=acc_type_var, values=["Recurring", "Salary"],
                                      state="readonly")
        acc_type_combo.grid(row=0, column=1, padx=5)

        # Change Address
        tk.Label(update_frame, text="New Address:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=1, column=0)
        new_address_entry = tk.Entry(update_frame, width=30)
        new_address_entry.grid(row=1, column=1, padx=5)

        # Optional: Gender selection
        tk.Label(update_frame, text="Gender:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=2, column=0)
        gender_var = tk.StringVar()
        tk.Radiobutton(update_frame, text="Male", variable=gender_var, value="Male", bg="#f0f4f7").grid(row=2, column=1,
                                                                                                        sticky="w")
        tk.Radiobutton(update_frame, text="Female", variable=gender_var, value="Female", bg="#f0f4f7").grid(row=2,
                                                                                                            column=1,
                                                                                                            padx=80,
                                                                                                            sticky="w")

        def fetch_details():
            username = self.logged_in_username
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
            username = self.logged_in_username
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

                    # Insert into transaction history for account type change
                    cursor.execute("""
                        INSERT INTO transaction_history (account_id, description, date)
                        SELECT a.account_id, %s, NOW()
                        FROM accounts a
                        JOIN users u ON a.user_id = u.user_id
                        WHERE u.username = %s
                    """, (f"Account type changed to {new_type}", username))

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
                    cursor.execute(
                        "DELETE FROM accounts WHERE user_id = (SELECT user_id FROM users WHERE username = %s)",
                        (username,))
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

        tk.Label(frame, text="📜 Transaction History", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Filter Section (In a single Frame neatly) ---
        filter_frame = tk.LabelFrame(self.root, text="🔎 Filter Options", bg="#f0f4f7", font=("Helvetica", 12, "bold"))
        filter_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=5,
                                                                                                           pady=5)
        start_entry = tk.Entry(filter_frame, width=20)
        start_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="End Date (YYYY-MM-DD):", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=0,
                                                                                                         column=2,
                                                                                                         padx=5, pady=5)
        end_entry = tk.Entry(filter_frame, width=20)
        end_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filter_frame, text="Transaction Type:", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=0, column=4,
                                                                                                    padx=5, pady=5)
        transaction_type_var = tk.StringVar()
        transaction_type_combo = ttk.Combobox(filter_frame, textvariable=transaction_type_var,
                                              values=["All", "Deposit", "Withdrawal"], state="readonly", width=17)
        transaction_type_combo.grid(row=0, column=5, padx=5, pady=5)
        transaction_type_combo.set("All")

        # --- Buttons neatly below Filters ---
        button_frame = tk.Frame(self.root, bg="#f0f4f7")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🔄 Refresh", font=("Helvetica", 11), width=18,
                  command=lambda: refresh_history()).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="⬇ Export to CSV", font=("Helvetica", 11), width=18,
                  command=lambda: export_to_csv()).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="⬅ Back to Dashboard", font=("Helvetica", 11), width=18,
                  command=self.dashboard).grid(row=0, column=2, padx=10)

        # --- Transaction Treeview ---
        columns = ("Account ID", "Full Name", "Branch", "Account Type", "Description", "Date")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_history():
            start_date = start_entry.get()
            end_date = end_entry.get()
            selected_type = transaction_type_var.get()

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

            if selected_type == "Deposit":
                query += " AND th.description LIKE %s"
                params.append("%Deposit%")
            elif selected_type == "Withdrawal":
                query += " AND th.description LIKE %s"
                params.append("%Withdrawal%")

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            records = cursor.fetchall()
            conn.close()

            # Clear previous rows
            for row in tree.get_children():
                tree.delete(row)

            # Insert latest rows
            for row in records:
                tree.insert("", "end", values=row)

        import os  # Make sure this is at the top of your script

        def export_to_csv():
            folder_path = r"D:\Smart_Bank_Management_system Project\transaction_history"
            os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

            selected_type = transaction_type_var.get()
            start_date = start_entry.get()
            end_date = end_entry.get()

            # Create a filename based on filters
            filename = "transaction_history"
            if selected_type != "All":
                filename = f"{selected_type}_transactions"
            if start_date and end_date:
                filename += f"_{start_date}_to_{end_date}"
            filename += ".csv"

            # Full path to save
            file_path = os.path.join(folder_path, filename)

            # Write CSV
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                for row_id in tree.get_children():
                    row = tree.item(row_id)['values']
                    writer.writerow(row)

            messagebox.showinfo("Export", f"📁 CSV exported successfully to:\n{file_path}")

        # Load initial data
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
