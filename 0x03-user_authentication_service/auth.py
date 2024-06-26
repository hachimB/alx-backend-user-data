#!/usr/bin/env python3
"""Module documentation"""
from user import User
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """hash a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """valid login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """method to create session"""
        # try:
        #     try:
        #         user = self._db.find_user_by(email=email)
        #         session_id = _generate_uuid()
        #         self._db.update_user(user.id, session_id=session_id)
        #         return session_id
        #     except NoResultFound:
        #         return None
        # except ValueError:
        #     return None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        try:
            self._db.update_user(user.id, session_id=session_id)
        except ValueError:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str):
        """method to get user from session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            return None
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str):
        """method to destroy session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """method to get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"The user {email} does not exist")
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """method to update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("User not found")
        new_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_password)
        self._db.update_user(user.id, reset_token=None)
