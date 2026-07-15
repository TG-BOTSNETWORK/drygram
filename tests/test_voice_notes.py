# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import VoiceNote

def test_voice_note_model():
    vn = VoiceNote(file_id="vn1", file_unique_id="vnu1", duration=15, waveform=b"\x01\x02", file_size=4000)
    assert vn.file_id == "vn1"
    assert vn.duration == 15
    assert vn.waveform == b"\x01\x02"
