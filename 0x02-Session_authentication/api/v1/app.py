#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.views.session_auth import session_auth_views
from flask import Flask, jsonify, abort, request
from importlib import import_module
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(session_auth_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()

if getenv('AUTH_TYPE') == 'basic_auth':
    BasicAuth = getattr(import_module("api.v1.auth.basic_auth"), 'BasicAuth')
    auth = BasicAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()

if getenv('AUTH_TYPE') == 'session_auth':
    SessionAuth = getattr(import_module("api.v1.auth.session_auth"),
                          'SessionAuth')
    auth = SessionAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorised(error):
    """ Unauthorised handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Access not allowed handler """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """ Before request handler """
    excluded_path = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/']
    if auth is None:
        return
    if auth.require_auth(request.path, excluded_path) is False:
        return
    if auth.authorization_header(request) is None:
        if auth.session_cookie(request) is None:
            abort(401)
    # if auth.current_user(request) is None:
    #     abort(403)
    try:
        request.current_user = auth.current_user(request)
        if request.current_user is None:
            abort(403)
    except Exception:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
