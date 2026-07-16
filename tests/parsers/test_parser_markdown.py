# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import MarkdownParser

def test_markdown_parser_all_entities():
    md = "__Underline__ and [Link](http://t.me)"
    text, entities = MarkdownParser.parse(md)
    assert text == "Underline and Link"
    assert len(entities) == 2
    types = [e["type"] for e in entities]
    assert "underline" in types
    assert "text_link" in types
