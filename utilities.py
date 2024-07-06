from argon2 import PasswordHasher
import sqlite3

conn = sqlite3.connect("passkeeper.db")
cursor = conn.cursor()
ph = PasswordHasher()

def add_account(account: str, username: str, password: str) -> bool:
    pw_hash = ph.hash(password)
    return True


def create_user(name: str, username: str, password: str) -> int:
    # Check if name, username, and password
    if not name or name.isspace():
        return 1

    if not username or username.isspace():
        return 2

    if not password or password.isspace():
        return 3

    # Check if the user currently exists
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
    # If the user exists, return false
    if not user.fetchone() is None:
        return 4

    # Add user, and return true
    pw_hash = ph.hash(password)
    cursor.execute("""
        INSERT INTO users(name, username, password) VALUES(?, ?, ?)
        """, (name, username, str(pw_hash), ))
    
    return 0


def delete_account(id: int):
    """TODO: Delete account"""


def verify_user(username: str, password: str) -> bool:
    # Get the hash
    pw_hash = cursor.execute("SELECT password FROM users WHERE username = ?", (username, ))

    # If there is no account, return false
    pw = pw_hash.fetchone()
    if pw is None:
        return False
    
    return ph.verify(pw[0], password)