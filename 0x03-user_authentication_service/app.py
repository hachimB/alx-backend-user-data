#!/usr/bin/env python3
"""Module documentation"""
from flask import Flask, jsonify, request, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
