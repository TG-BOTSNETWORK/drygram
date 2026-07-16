# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Topic

def test_topic_model():
    topic = Topic(id=1, name="General", icon_color=0xFFFFFF, icon_emoji_id=5)
    assert topic.id == 1
    assert topic.name == "General"
    assert topic.icon_color == 0xFFFFFF
    assert topic.icon_emoji_id == 5
