import argon2


def add_account(account: str, username: str, password: str) -> bool:
    pw_hash = argon2.hash_password(password)
    return True


def create_user(username: str, name: str, password: str) -> bool:
    """TODO: Add user to local database"""


def delete_account(id: int):
    """TODO: Delete account"""


def verify_user(username: str, password: str) -> bool:
    """TODO: Check if the user exists"""
    return True