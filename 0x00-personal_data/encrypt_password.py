#!/usr/bin/env python3
"""Encrypting passwords"""
from bcrypt import gensalt, hashpw


def hash_password(password: str) -> bytes:
    """Hashing a password"""
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    byte = password.encode('utf-8')
    salt = gensalt()
    hashed = hashpw(byte, salt)
    return hashed
