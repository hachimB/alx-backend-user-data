#!/usr/bin/env python3
"""Module documentation"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        # user_email = self._db._session.query(
        #     User).filter_by(email=email).first()
        user = User(email=email, hashed_password=_hash_password(password))
        if user:
            raise ValueError(f"User {email} already exists")
        else:
            # user = User(email=email, hashed_password=_hash_password(password))
            # user.email = email
            # user.hashed_password = _hash_password(password)
            self._db._session.add(user)
            self._db._session.commit()
            return user
