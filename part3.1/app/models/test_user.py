#!/usr/bin/python3

from user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="johndelpueblo@ejemplo.com")
    print(user)
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "johndelpueblo@ejemplo.com"
    assert user.is_admin is False

test_user_creation()
