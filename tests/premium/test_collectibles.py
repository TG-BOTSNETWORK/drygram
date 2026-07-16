# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Collectible

def test_collectible_properties():
    col = Collectible(id="col1", title="NiceUsername", type="username", address="t.me/NiceUsername")
    assert col.title == "NiceUsername"
    assert col.type == "username"
    assert col.address == "t.me/NiceUsername"
