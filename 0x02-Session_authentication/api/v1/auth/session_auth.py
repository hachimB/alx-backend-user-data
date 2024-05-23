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
        id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user_id for a given session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

