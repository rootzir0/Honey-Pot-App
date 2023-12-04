import sqlite3

# Connect to the database (this will create a new file named 'password_app.db' if it doesn't exist)
conn = sqlite3.connect('password_app.db')
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

# Create a table for third-party accounts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS third_party_accounts (
        account_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        account_name TEXT NOT NULL,
        account_username TEXT NOT NULL,
        account_password TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    )
''')

import sqlite3
from sqlite3 import Error

DB_FILE = 'password_app.db'

def create_connection():
    """Create a database connection to SQLite."""
    connection = None
    try:
        connection = sqlite3.connect(DB_FILE)
        print(f"Connected to the database: {DB_FILE}")
        return connection
    except Error as e:
        print(e)

    return connection

def close_connection(connection):
    """Close the database connection."""
    if connection:
        connection.close()
        print("Connection to the database closed.")

def create_user(username, password_hash):
    """Create a new user."""
    connection = create_connection()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            print(f"User {username} created successfully.")
    except Error as e:
        print(e)
    finally:
        close_connection(connection)

def add_third_party_account(user_id, account_name, account_username, account_password):
    """Add a third-party account for a user."""
    connection = create_connection()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO third_party_accounts (user_id, account_name, account_username, account_password)
                VALUES (?, ?, ?, ?)
            """, (user_id, account_name, account_username, account_password))
            print(f"Third-party account {account_name} added successfully for user {user_id}.")
    except Error as e:
        print(e)
    finally:
        close_connection(connection)

def update_user_password(user_id, new_password_hash):
    """Update a user's password."""
    connection = create_connection()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_password_hash, user_id))
            print(f"Password for user {user_id} updated successfully.")
    except Error as e:
        print(e)
    finally:
        close_connection(connection)

# Commit the changes and close the connection
conn.commit()
conn.close()