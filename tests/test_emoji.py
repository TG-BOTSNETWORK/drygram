# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import PremiumEmojiStatus

def test_premium_emoji_status():
    status = PremiumEmojiStatus(emoji_id="emoji_abc", expiration_date=1700000000)
    assert status.emoji_id == "emoji_abc"
    assert status.expiration_date == 1700000000
