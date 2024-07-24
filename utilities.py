from argon2 import PasswordHasher, exceptions
import sqlite3
from cryptography.fernet import Fernet

conn = sqlite3.connect("passkeeper.db")
cursor = conn.cursor()
ph = PasswordHasher()


def create_account(user_id: int, service: str, username: str, password: str) -> int:
    # Check if service, username, and password are valid
    if not service or service.isspace():
        return 1
    
    username = username.strip(" ")
    if not username or username.isspace() or username.find(" ") != -1:
        return 2
    
    if not password or password.isspace() or password.find(" ") != -1:
        return 3
    
    account = cursor.execute("SELECT * FROM accounts WHERE service = ? AND username = ?", (service, username))
    if not account.fetchone() is None:
        return 4

    key = cursor.execute("SELECT pkey FROM users WHERE id = ?", (user_id, )).fetchone()
    fernet = Fernet(key[0])
    pw_encrypt = fernet.encrypt(password.encode())
    cursor.execute("""
        INSERT INTO accounts(user_id, service, username, hash) VALUES(?, ?, ?, ?)
        """, (user_id, service, username, str(pw_encrypt.decode()), ))    

    return 0


def create_user(name: str, username: str, password: str) -> int:
    # Check if name, username, and password are valid
    if not name or name.isspace():
        return 1

    username = username.strip(" ")
    if not username or username.isspace() or username.find(" ") != -1:
        return 2

    if not password or password.isspace() or password.find(" ") != -1:
        return 3

    # Check if the user currently exists
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
    # If the user exists, return false
    if not user.fetchone() is None:
        return 4

    # Add user, and return true
    pw_hash = ph.hash(password)
    key = Fernet.generate_key()
    cursor.execute("""
        INSERT INTO users(name, username, password, pkey) VALUES(?, ?, ?, ?)
        """, (name, username, str(pw_hash), key, ))
    
    return 0


def decrypt_password(user_id: int, password: bytes) -> str:
    key = cursor.execute("SELECT pkey FROM users WHERE id = ?", (user_id, )).fetchone()
    fernet = Fernet(key[0])
    return fernet.decrypt(password).decode()


def delete_account(account_id: int) -> None:
    return cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id, ))


def get_accounts(user_id: int):
    return cursor.execute("SELECT id, user_id, service, username, hash FROM accounts WHERE user_id = ? ORDER BY service ASC", (user_id, ))


def get_name(user_id: int) -> str:
    q = cursor.execute("SELECT name FROM users WHERE id = ?", (user_id, ))
    name = q.fetchone()
    return str(name[0])


def get_user_id(username: str) -> int:
    q = cursor.execute("SELECT id FROM users WHERE username = ?", (username, ))
    user_id = q.fetchone()
    return int(user_id[0])


def verify_user(username: str, password: str) -> bool:
    # Get the hash
    pw_hash = cursor.execute("SELECT password FROM users WHERE username = ?", (username, ))

    # If there is no account, return false
    pw = pw_hash.fetchone()
    if pw is None:
        return False
    
    # Verify the user
    try:
        return ph.verify(pw[0], password)
    except exceptions.VerifyMismatchError:
        return False