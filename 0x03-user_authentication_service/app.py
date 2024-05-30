#!/usr/bin/env python3
"""Module documentation"""
from flask import Flask, jsonify, request, abort,\
    make_response, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Users route"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return {"email": f"{email}", "message": "user created"}
    except ValueError:
        return {"message": "email already registered"}, 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout route"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    else:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
        else:
            abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Profile route"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Reset password route"""
    email = request.form.get('email')
    if not email:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    if token:
        return {"email": email, "reset_token": token}, 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
