# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Document

def test_sticker_model():
    sticker = Document(file_id="sticker_123", file_unique_id="s123", file_name="sticker.webp", mime_type="image/webp", file_size=5000)
    assert sticker.file_id == "sticker_123"
    assert sticker.mime_type == "image/webp"
