#!/usr/bin/env python3
"""Module documentation"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
