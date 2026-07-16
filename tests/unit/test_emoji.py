# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
from drygram import Emoji, EmojiCategory, EmojiLookup, EmojiParser, EmojiFormatter, EmojiDatabase

def test_emoji_database_lookup():
    EmojiDatabase.initialize()
    
    # Test lookup of standard grinning face emoji
    emoji = EmojiDatabase.get("😀")
    assert emoji is not None
    assert emoji.char == "😀"
    assert emoji.category == EmojiCategory.SMILEYS
    assert emoji.code_point == "U+1F600"
    
    # Test lookup by shortcode
    emoji_by_sc = EmojiDatabase.get(":grinning_face:")
    assert emoji_by_sc is not None
    assert emoji_by_sc.char == "😀"
    
    # Test searching
    results = EmojiDatabase.search("grinning")
    assert len(results) > 0
    assert any(e.char == "😀" for e in results)

def test_emoji_lookup_methods():
    assert EmojiLookup.to_emoji(":grinning_face:") == "😀"
    assert EmojiLookup.to_shortcode("😀") == ":grinning_face:"
    assert EmojiLookup.to_unicode("😀") == "U+1F600"

def test_emoji_parser_and_formatter():
    text = "Hello 😀 world!"
    
    # Parse emojis in text
    parsed = EmojiParser.parse(text)
    assert len(parsed) == 1
    assert parsed[0].char == "😀"
    
    # Demojize formatting
    demojized = EmojiFormatter.demojize(text)
    assert demojized == "Hello :grinning_face: world!"
    
    # Replace shortcodes back
    reconstructed = EmojiParser.replace_shortcodes(demojized)
    assert reconstructed == text
