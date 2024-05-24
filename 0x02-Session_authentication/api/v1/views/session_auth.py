#!/usr/bin/env python3
"""session authentication"""
from flask import Blueprint, request, jsonify, make_response
from api.v1.views.users import User
import os


session_auth_views = Blueprint(
    "session_auth_views",
    __name__,
    url_prefix="/api/v1")


@session_auth_views.route('/auth_session/login',
                          methods=['POST'], strict_slashes=False)
def login():
    """login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    # if not email:
    #     return jsonify({"error": "email missing"}), 400
    # if not password:
    #     return jsonify({"error": "password missing"}), 400
    # users = User.search({"email": email})
    # if not users:
    #     return jsonify({"error": "no user found for this email"}), 404

    # user = users[0]
    # if not user.is_valid_password(password):
    #     return jsonify({"error": "wrong password"}), 401

    # from api.v1.app import auth
    # session_id = auth.create_session(user.id)

    # response = make_response(user.to_json())
    # response.set_cookie(os.getenv('SESSION_NAME'), session_id)

    # return response
    # Check if email is provided
    if not email:
        # Return error message if email is missing
        return jsonify({"error": "email missing"}), 400

    # Check if password is provided
    if not password:
        # Return error message if password is missing
        return jsonify({"error": "password missing"}), 400

    # Search for users with the provided email
    users = User.search({"email": email})

    # Check if any users were found
    if not users:
        # Return error message if no users were found
        return jsonify({"error": "no user found for this email"}), 404

    # Get the first user from the list of users
    user = users[0]

    # Check if the provided password is valid
    if not user.is_valid_password(password):
        # Return error message if the password is invalid
        return jsonify({"error": "wrong password"}), 401

    # Import the auth module and create a session ID for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Create a response with the JSON representation of the user
    response = make_response(user.to_json())

    # Set a cookie with the session ID in the response
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)

    # Return the response
    return response
