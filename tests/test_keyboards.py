# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import KeyboardButton, ReplyKeyboardMarkup

def test_reply_keyboard_markup():
    btn = KeyboardButton(text="Send Contact", request_contact=True)
    markup = ReplyKeyboardMarkup(keyboard=[[btn]])
    assert len(markup.keyboard) == 1
    assert markup.keyboard[0][0].text == "Send Contact"
    assert markup.keyboard[0][0].request_contact is True
