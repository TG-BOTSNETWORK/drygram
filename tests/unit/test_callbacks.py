# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import InlineKeyboardButton

def test_callback_button():
    btn = InlineKeyboardButton(text="Click", callback_data="data1")
    assert btn.text == "Click"
    assert btn.callback_data == "data1"
