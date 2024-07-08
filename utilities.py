from argon2 import PasswordHasher
import sqlite3


conn = sqlite3.connect("passkeeper.db")
cursor = conn.cursor()
ph = PasswordHasher()


def create_account(user_id: int, service: str, username: str, password: str) -> int:
    if not service or service.isspace():
        return 1
    
    if not username or username.isspace():
        return 2
    
    if not password or password.isspace():
        return 3
    
    account = cursor.execute("SELECT * FROM accounts WHERE service = ? AND username = ?", (service, username))
    if account.fetchone() is None:
        return 4

    pw_hash = ph.hash(password)
    cursor.execute("""
        INSERT INTO accounts(user_id, service, username, hash) VALUES(?, ?, ?, ?)
        """, (user_id, service, username, str(pw_hash), ))    

    return 0


def create_user(name: str, username: str, password: str) -> int:
    # Check if name, username, and password is valid
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


def get_user_id(username: str) -> int:
    q = cursor.execute("SELECT id FROM users WHERE username = ?", (username, ))
    user_id = q.fetchone()
    return int(user_id[0])


def get_name(user_id: int) -> str:
    q = cursor.execute("SELECT name FROM users WHERE id = ?", (user_id, ))
    name = q.fetchone()
    return str(name[0])


def get_accounts(user_id: int):
    return cursor.execute("SELECT id, service, username, password FROM accounts WHERE user_id = ?", (user_id, ))


def delete_account(account_id: int) -> None:
    return cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id, ))


def verify_user(username: str, password: str) -> bool:
    # Get the hash
    pw_hash = cursor.execute("SELECT password FROM users WHERE username = ?", (username, ))

    # If there is no account, return false
    pw = pw_hash.fetchone()
    if pw is None:
        return False
    
    # Verify the user
    return ph.verify(pw[0], password)