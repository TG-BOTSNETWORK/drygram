# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Photo, Video, Document

def test_media_properties():
    photo = Photo(file_id="p1", file_unique_id="pu1", width=10, height=20, file_size=100)
    assert photo.file_id == "p1"
    assert photo.width == 10
    
    video = Video(file_id="v1", file_unique_id="vu1", width=30, height=40, duration=5, file_size=200)
    assert video.duration == 5
    
    doc = Document(file_id="d1", file_unique_id="du1", file_name="n.txt", mime_type="text/plain", file_size=50)
    assert doc.file_name == "n.txt"
