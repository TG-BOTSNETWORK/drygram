# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import BusinessConnection, BusinessLink, BusinessGreeting

def test_business_models():
    conn = BusinessConnection(id="conn1", user_id=123, dc_id=1, can_reply=True)
    assert conn.id == "conn1"
    assert conn.can_reply is True
    
    link = BusinessLink(url="http://t.me/b/1", message="hello", views=5)
    assert link.views == 5
    
    greet = BusinessGreeting(message="Welcome!")
    assert greet.message == "Welcome!"
