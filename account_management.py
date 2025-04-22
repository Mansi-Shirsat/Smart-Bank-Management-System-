#Account_management
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db_config import mysql


class AccountManager:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.db_connection = mysql()

        # Create UI elements
        self.account_type_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.gender_var = tk.StringVar()

    def account_management_ui(self):
        self.clear_screen()

        title = tk.Label(self.root, text="Account Management", font=("Helvetica", 18, "bold"))
        title.pack(pady=20)

        # Fetch account details from the database
        account_details = self.get_account_details(self.user_id)

        if not account_details:
            messagebox.showerror("Error", "Account details not found.")
            return

        # Create fields to display and update account details
        account_id_label = tk.Label(self.root, text="Account ID: " + str(account_details['account_id']))
        account_id_label.pack(pady=10)

        # Account Type (Dropdown to select Recurring/Salary)
        account_type_label = tk.Label(self.root, text="Account Type:")
        account_type_label.pack()
        account_type_options = ['Savings', 'Current', 'Recurring', 'Salary']
        self.account_type_var.set(account_details['account_type'])
        account_type_dropdown = tk.OptionMenu(self.root, self.account_type_var, *account_type_options)
        account_type_dropdown.pack(pady=10)

        # Address Field
        address_label = tk.Label(self.root, text="Address:")
        address_label.pack()
        self.address_var.set(account_details['address'])
        address_entry = tk.Entry(self.root, textvariable=self.address_var, width=50)
        address_entry.pack(pady=10)

        # Gender Field (Radio Buttons for Male/Female/Other)
        gender_label = tk.Label(self.root, text="Gender:")
        gender_label.pack()
        gender_options = ['Male', 'Female', 'Other']
        self.gender_var.set(account_details['gender'])
        gender_frame = tk.Frame(self.root)
        for gender in gender_options:
            gender_rb = tk.Radiobutton(gender_frame, text=gender, value=gender, variable=self.gender_var)
            gender_rb.pack(side=tk.LEFT)
        gender_frame.pack(pady=10)

        # Update Button
        update_button = tk.Button(self.root, text="Update", command=self.update_account_details)
        update_button.pack(pady=20)

    def update_account_details(self):
        account_type = self.account_type_var.get()
        address = self.address_var.get()
        gender = self.gender_var.get()

        # Validate inputs
        if not account_type or not address or not gender:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Update the database
        try:
            cursor = self.db_connection.cursor()
            query = """
                UPDATE accounts
                SET account_type = %s, address = %s, gender = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (account_type, address, gender, self.user_id))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Account details updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating account details: {err}")
        finally:
            cursor.close()

    def get_account_details(self, user_id):
        # Fetch account details for a user
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM accounts WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            account_details = cursor.fetchone()
            return account_details
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching account details: {err}")
            return None
        finally:
            cursor.close()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
