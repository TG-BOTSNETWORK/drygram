# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Photo

def test_photo_model():
    photo = Photo(file_id="p1", file_unique_id="pu1", width=640, height=480, file_size=45000)
    assert photo.file_id == "p1"
    assert photo.width == 640
    assert photo.height == 480
