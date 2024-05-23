#!/usr/bin/env python3
"""Session authentication"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a user"""
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid.uuid4()
        SessionAuth.user_id_by_session_id[id] = user_id
        return id
