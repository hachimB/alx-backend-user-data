#!/usr/bin/env python3
"""Session authentication"""
from api.v1.auth.auth import Auth
from models.user import User
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

    def current_user(self, request=None):
        """current_user function"""
        _my_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(_my_session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes a session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if session_id != self.user_id_for_session_id(session_id):
            return False
        else:
            del SessionAuth.user_id_by_session_id[session_id]
            return True
