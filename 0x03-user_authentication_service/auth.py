#!/usr/bin/env python3
"""Module documentation"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
        try:
            user_email = self._db.find_user_by(email=email)
            if user_email:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = User(email=email, hashed_password=_hash_password(password))
            self._db.add_user(user.email, user.hashed_password)
            return user
