# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import HTMLParser

def test_html_parser_all_tags():
    html = '<u>Underline</u> and <a href="http://t.me">Link</a>'
    text, entities = HTMLParser.parse(html)
    assert text == "Underline and Link"
    assert len(entities) == 2
    types = [e["type"] for e in entities]
    assert "underline" in types
    assert "text_link" in types
