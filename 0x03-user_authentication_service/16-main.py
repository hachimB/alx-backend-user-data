#!/usr/bin/env python3
from auth import Auth  # replace with the actual module name
from db import DB

def main():
    auth = Auth()  # replace with the actual initialization if needed
    my_db = DB()
    email = 'bob@bob.com'  # replace with a valid email
    hashed_password = '123456'  # replace with a valid password
    user = my_db.add_user(email, hashed_password)
    if user:
        print(f'User {email} created successfully.')
    else:
        print(f'Failed to create user {email}.')
        return

    # Test update_user method
    try:
        my_db.update_user(user.id, hashed_password='new_password')
        print(f'User {email} updated successfully.')
    except ValueError:
        print(f'Failed to update user {email}.')

    try:
        token = auth.get_reset_password_token(email)
        print(f'Reset token for {email}: {token}')
    except ValueError:
        print(f'No user found with email {email}')

if __name__ == '__main__':
    main()