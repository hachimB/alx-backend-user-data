#!/usr/bin/env python3
"""Encrypting passwords"""
from bcrypt import gensalt, hashpw


# def hash_password(password: str) -> bytes:
#     """Hashing a password"""
#     byte = password.encode('utf-8')
#     salt = gensalt()
#     hashed = hashpw(byte, salt)
#     return hashed
def hash_password(password: str) -> bytes:
    """Hashing a password"""
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    try:
        byte = password.encode('utf-8')
        salt = gensalt()
        hashed = hashpw(byte, salt)
    except Exception as e:
        raise RuntimeError("An error occurred while hashing the password") from e
    return hashed
