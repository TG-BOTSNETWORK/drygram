# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import InlineKeyboardButton

def test_inline_button_model():
    btn = InlineKeyboardButton(text="Go", url="http://example.com")
    assert btn.text == "Go"
    assert btn.url == "http://example.com"
    assert btn.callback_data is None
