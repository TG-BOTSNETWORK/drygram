# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import PremiumEmojiStatus

def test_premium_models():
    status = PremiumEmojiStatus(emoji_id="emoji_123")
    assert status.emoji_id == "emoji_123"
    assert status.document_id is None
