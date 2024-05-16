#!/usr/bin/env python3
"""Encrypting passwords"""
from bcrypt import gensalt, hashpw # type: ignore


def hash_password(password: str) -> bytes:
    """Hashing a password"""
    byte = password.encode('utf-8')
    salt = gensalt()
    hashed = hashpw(byte, salt)
    return hashed
