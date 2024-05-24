#!/usr/bin/env python3
"""Documentation:
session authentication"""
from flask import Blueprint, request, jsonify, make_response, abort
from api.v1.views.users import User
from api.v1.app import auth
import os


session_auth_views = Blueprint(
    "session_auth_views",
    __name__,
    url_prefix="/api/v1")


@session_auth_views.route('/auth_session/login',
                          methods=['POST'], strict_slashes=False)
def login():
    """Documentation for login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = make_response(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return response


@session_auth_views.route('/auth_session/logout',
                          method=['DELETE'], strict_slashes=False)
def logout():
    """Documentation for logout"""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
