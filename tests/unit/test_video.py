# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Video

def test_video_model():
    vid = Video(file_id="v1", file_unique_id="vu1", width=1920, height=1080, duration=60, file_size=1500000)
    assert vid.file_id == "v1"
    assert vid.width == 1920
    assert vid.height == 1080
    assert vid.duration == 60
