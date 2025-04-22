import mysql.connector
from hashlib import sha256
from tkinter import messagebox

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Adjust to your DB host if needed
        user="root",       # Replace with your MySQL username
        password="Learn@02mysql",       # Replace with your MySQL password
        database="smart_bank"
    )

# Hash password for security
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Registration Function
def register_user(user_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (user_data["username"],))
        if cursor.fetchone():
            messagebox.showerror("Error", "❌ Username already exists!")
            return False

        # Hash the password before saving
        hashed_password = hash_password(user_data["password"])

        # Insert new user data into the 'users' table
        query = """
            INSERT INTO users (username, password_hash, full_name, gender, dob, phone, address, pan, account_type, deposit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data["username"],
            hashed_password,
            user_data["full_name"],
            user_data["gender"],
            user_data["dob"],
            user_data["phone"],
            user_data["address"],
            user_data["pan"],
            user_data["account_type"],
            user_data["deposit"]
        ))

        conn.commit()
        messagebox.showinfo("Success", "✅ User registered successfully!")
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"❌ Database error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Login Function
def login_user(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Hash the entered password
        hashed_password = hash_password(password)

        # Query the database to check if the username and hashed password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            return True  # Login successful
        else:
            messagebox.showerror("Error", "❌ Invalid credentials!")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"❌ Database error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Password Reset Function
def reset_user_password(username, phone, pan, new_password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Hash the new password before saving
        hashed_password = hash_password(new_password)

        # Check if the provided details match any user
        cursor.execute("SELECT * FROM users WHERE username = %s AND phone = %s AND pan = %s", (username, phone, pan))
        user = cursor.fetchone()

        if user:
            # Update the password in the 'users' table
            cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (hashed_password, username))
            conn.commit()
            messagebox.showinfo("Success", "✅ Password reset successful!")
            return True
        else:
            messagebox.showerror("Error", "❌ Invalid details provided!")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"❌ Database error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Get User Details Function (e.g., for Account Management)
def get_user_details(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user details from the 'users' table
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return {
                "username": user[0],  # Assuming username is the first column
                "full_name": user[2],
                "gender": user[3],
                "dob": user[4],
                "phone": user[5],
                "address": user[6],
                "pan": user[7],
                "account_type": user[8],
                "deposit": user[9]
            }
        else:
            messagebox.showerror("Error", "❌ User not found!")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"❌ Database error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# Update User Details Function (e.g., for Account Management)
def update_user_details(username, updated_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Construct the UPDATE query
        query = """
            UPDATE users
            SET full_name = %s, gender = %s, dob = %s, phone = %s, address = %s, pan = %s, account_type = %s, deposit = %s
            WHERE username = %s
        """
        cursor.execute(query, (
            updated_data["full_name"],
            updated_data["gender"],
            updated_data["dob"],
            updated_data["phone"],
            updated_data["address"],
            updated_data["pan"],
            updated_data["account_type"],
            updated_data["deposit"],
            username
        ))

        conn.commit()
        messagebox.showinfo("Success", "✅ User details updated successfully!")
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"❌ Database error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
