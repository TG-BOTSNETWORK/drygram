# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import User

def test_user_properties():
    user = User(id=999, first_name="John", last_name="Doe", username="johndoe", is_bot=False)
    assert user.id == 999
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.username == "johndoe"
    assert user.is_bot is False
