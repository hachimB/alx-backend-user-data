#!/usr/bin/env python3
"""Basic auth"""
from .auth import Auth
from typing import Tuple, TypeVar, Optional
from flask import request
import base64
from models.base import Base
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header"""
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """decode_base64_authorization_header"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header)
        except Exception as e:
            return None
        return base64_bytes.decode('utf-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """extract_user_credentials"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        authorization_header = decoded_base64_authorization_header.split(':')
        return (authorization_header[0], authorization_header[1])

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> Optional['User']:
        """user_object_from_credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None):
        """current_user"""
        # Get the authorization header
        auth_header = self.authorization_header(request)

        # Extract the Base64 part of the authorization header
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)

        # Decode the Base64 part
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)

        # Extract the user credentials from the decoded Base64 part
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_auth_header)

        # Retrieve the User instance for these credentials
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
