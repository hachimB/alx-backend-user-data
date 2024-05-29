#!/usr/bin/env python3
"""Module documentation"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
