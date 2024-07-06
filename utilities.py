import argon2
import sqlite3

conn = sqlite3.connect("passkeeper.db")
cursor = conn.cursor()


def add_account(account: str, username: str, password: str) -> bool:
    pw_hash = argon2.hash_password(password)
    return True


def create_user(name: str, username: str, password: str) -> bool:
    # Check if the user currently exists
    user = cursor.execute("SELECT name FROM users WHERE username = ?", username)
    # If the user exists, return false
    if not (user.fetchone() is None):
        return False

    # Add user, and return true
    pw_hash = argon2.hash_password(password)
    cursor.execute("""
        INSERT INTO users(name, username, password) VALUES(?, ?, ?)
        """, name, username, str(pw_hash))
    
    return True


def delete_account(id: int):
    """TODO: Delete account"""


def verify_user(username: str, password: str) -> bool:
    """TODO: Check if the user exists"""
    return True