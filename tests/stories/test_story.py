# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Story, StoryReaction, StoryPrivacy

def test_story_creation():
    privacy = StoryPrivacy(privacy_type="contacts")
    reaction = StoryReaction(emoji="🔥", count=5)
    story = Story(id=1, sender_id=123, media=None, caption="hello", date=100, privacy=privacy, reactions=[reaction])
    assert story.id == 1
    assert story.caption == "hello"
    assert story.privacy.privacy_type == "contacts"
    assert story.reactions[0].emoji == "🔥"
