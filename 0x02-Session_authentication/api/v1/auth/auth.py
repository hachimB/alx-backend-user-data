#!/usr/bin/env python3
"""Auth class"""
from typing import List, TypeVar
from flask import Flask, request
import os


class Auth:
    """Auth class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path is in excluded paths"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path = path + '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Get authorization header"""
        auth_header = request.headers.get('Authorization')
        if not request or not auth_header:
            return None
        return auth_header

    def current_user(self, request=None):
        """current_user"""
        return None

    def session_cookie(self, request=None):
        """Returns the session cookie"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        if not session_name:
            return None
        _my_session_id = request.cookies.get(session_name)
        return _my_session_id
