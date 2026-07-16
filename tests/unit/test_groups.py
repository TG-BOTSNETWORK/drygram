# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Chat

def test_group_chat():
    group = Chat(id=-10012345, type="supergroup", title="DryGram Group")
    assert group.id == -10012345
    assert group.type == "supergroup"
    assert group.title == "DryGram Group"
