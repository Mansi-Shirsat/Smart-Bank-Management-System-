import mysql.connector


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Learn@02mysql",
}

try:
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create a new database
    database_name = "SmartBankDB"  # Change this to your preferred name
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"✅ Database '{database_name}' created successfully!")

    # Close cursor and connection
    cursor.close()
    conn.close()
    print("✅ Connection closed.")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
