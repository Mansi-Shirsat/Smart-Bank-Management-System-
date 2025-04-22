import hashlib

from db_config import get_connection
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

from datetime import datetime

def register_user(user_data):
    try:
        # Hash the password
        password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()

        if user_data['password'] != user_data['confirm_password']:
            print("Passwords do not match.")
            return False

        # Validate account type
        if user_data['account_type'] not in ['Savings', 'Current']:
            print("Invalid account type.")
            return False

        conn = get_connection()
        cursor = conn.cursor()

        # Insert into users table
        insert_user = """
        INSERT INTO users 
        (full_name, username, password_hash, dob, phone, address, pan, account_type, deposit, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        user_values = (
            user_data['full_name'],
            user_data['username'],
            password_hash,
            user_data['dob'],
            user_data['phone'],
            user_data['address'],
            user_data['pan'],
            user_data['account_type'],
            float(user_data['deposit']),
            user_data['gender']
        )

        cursor.execute(insert_user, user_values)
        conn.commit()

        # Get the new user_id
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (user_data['username'],))
        result = cursor.fetchone()
        if not result:
            print("User insertion failed.")
            return False
        user_id = result[0]

        # Insert into accounts table
        insert_account = """
        INSERT INTO accounts (user_id, account_type, balance, branch_name, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        account_values = (
            user_id,
            user_data['account_type'],
            float(user_data['deposit']),
            "Main Branch",  # Default or update later
            datetime.now()
        )
        cursor.execute(insert_account, account_values)
        conn.commit()

        return True

    except Exception as e:
        print("Registration error:", e)
        return False

    finally:
        if conn:
            conn.close()
