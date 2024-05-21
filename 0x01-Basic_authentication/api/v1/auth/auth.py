#!/usr/bin/env python3
"""Auth class"""
from typing import List, TypeVar
from flask import Flask, request


class Auth:
    """Auth class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path is in excluded paths"""
        return False

    def authorization_header(self, request=None) -> str:
        """Get authorization header"""
        return None

    def current_user(self, request=None):
        """current_user"""
        return None
