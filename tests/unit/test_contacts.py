# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import User

def test_contact_user():
    user = User(id=888, first_name="ContactName")
    assert user.id == 888
    assert user.first_name == "ContactName"
    assert user.username is None
