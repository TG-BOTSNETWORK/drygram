# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Document

def test_document_model():
    doc = Document(file_id="d1", file_unique_id="du1", file_name="notes.pdf", mime_type="application/pdf", file_size=1024)
    assert doc.file_id == "d1"
    assert doc.file_name == "notes.pdf"
    assert doc.mime_type == "application/pdf"
