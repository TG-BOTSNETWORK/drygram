# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Gift, GiftUpgrade

def test_gifts_properties():
    gift = Gift(id="g1", name="Birthday", emoji="🎂", cost_stars=100)
    assert gift.id == "g1"
    assert gift.is_upgraded is False
    
    upgrade = GiftUpgrade(id="gu1", gift_id="g1", new_emoji="🎆", upgrade_cost_stars=50)
    assert upgrade.new_emoji == "🎆"
    assert upgrade.upgrade_cost_stars == 50
