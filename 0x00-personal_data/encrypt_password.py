#!/usr/bin/env python3
"""Encrypting passwords"""
from bcrypt import gensalt, hashpw, checkpw


def hash_password(password: str) -> bytes:
    """Hashing a password"""
    byte = password.encode('utf-8')
    salt = gensalt()
    hashed = hashpw(byte, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check valid password"""
    provided_passwd = password.encode('utf-8')
    return checkpw(provided_passwd, hashed_password)
