# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Audio

def test_audio_model():
    audio = Audio(file_id="a1", file_unique_id="au1", duration=180, performer="Santhu", title="DryGram Anthem", file_size=300000)
    assert audio.file_id == "a1"
    assert audio.duration == 180
    assert audio.performer == "Santhu"
    assert audio.title == "DryGram Anthem"
