# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import MarkdownParser, HTMLParser

def test_parsers_cross_verification():
    text_md, ents_md = MarkdownParser.parse("**Hello**")
    text_html, ents_html = HTMLParser.parse("<b>Hello</b>")
    assert text_md == text_html == "Hello"
    assert ents_md[0]["type"] == ents_html[0]["type"] == "bold"
