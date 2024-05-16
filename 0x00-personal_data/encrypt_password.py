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
    byte: bytes = password.encode('utf-8')
    salt: bytes = gensalt()
    hashed: bytes = hashpw(byte, salt)
    return hashed
