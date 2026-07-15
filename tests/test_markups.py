# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import InlineKeyboardMarkup, InlineKeyboardButton

def test_inline_keyboard_markup():
    btn = InlineKeyboardButton(text="Click", callback_data="cb")
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    assert len(markup.inline_keyboard) == 1
    assert markup.inline_keyboard[0][0].callback_data == "cb"
