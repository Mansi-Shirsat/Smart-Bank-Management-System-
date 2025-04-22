import mysql.connector

def get_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Or your actual username
        password="Learn@02mysql",  # Password you used in CLI
        database="smart_bank"  # Ensure this DB exists
    )

