# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Chat

def test_chat_boosts():
    chat = Chat(id=-100123, type="channel")
    assert chat.id == -100123
    assert chat.type == "channel"
