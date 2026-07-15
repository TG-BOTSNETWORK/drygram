# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Chat

def test_channel_chat():
    channel = Chat(id=-10055555, type="channel", title="DryGram Channel", username="drygram_channel")
    assert channel.id == -10055555
    assert channel.type == "channel"
    assert channel.username == "drygram_channel"
