#!/usr/bin/env python3
"""Module documentation"""
import requests


def register_user(email: str, password: str) -> None:
    """Register user"""
    response = requests.post(
        'http://localhost:5000/users',
        data={
            'email': email,
            'password': password})
    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 200
    assert response.json() == {"email": f"{email}", "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password"""
    response = requests.post(
        'http://localhost:5000/sessions',
        data={
            'email': email,
            'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in"""
    response = requests.post(
        'http://localhost:5000/sessions',
        data={
            'email': email,
            'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Profile unlogged"""
    response = requests.get('http://localhost:5000/profile')
    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 403
    assert response.cookies.get('session_id') is None


def profile_logged(session_id: str) -> None:
    """Profile logged"""
    response = requests.get(
        'http://localhost:5000/profile',
        cookies={
            'session_id': session_id})
    assert response.status_code == 200
    email = response.json().get("email")
    assert email is not None
    assert response.json() == {"email": email}


def log_out(session_id: str) -> None:
    """Log out"""
    response = requests.delete(
        'http://localhost:5000/profile',
        cookies={
            'session_id': session_id})
    assert response.status_code == 403


def reset_password_token(email: str) -> str:
    """Reset password token"""
    response = requests.post(
        'http://localhost:5000/reset_password',
        data={
            'email': email})
    assert response.status_code == 200
    token = response.json().get('reset_token')
    assert response.json() == {"email": email, "reset_token": token}
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    response = requests.put(
        'http://localhost:5000/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'password': new_password})
    assert response.status_code == 200
    assert response.json() == {
        "email": f"{email}",
        "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
