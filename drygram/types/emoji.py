# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import unicodedata
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

# EMOJI UNICODE BLOCKS FOR RUNTIME LOOKUP
EMOJI_RANGES = [
    (0x1F600, 0x1F64F), # Emoticons
    (0x1F300, 0x1F5FF), # Misc Symbols and Pictographs
    (0x1F680, 0x1F6FF), # Transport and Map Symbols
    (0x1F900, 0x1F9FF), # Supplemental Symbols and Pictographs
    (0x1FA70, 0x1FAFF), # Symbols and Pictographs Extended-A
    (0x2600, 0x26FF),   # Misc Symbols
    (0x2700, 0x27BF),   # Dingbats
    (0x1F1E6, 0x1F1FF), # Regional Indicators (Flags)
]

class EmojiCategory:
    SMILEYS = "Smileys & Emotion"
    PEOPLE = "People & Body"
    ANIMALS = "Animals & Nature"
    FOOD = "Food & Drink"
    TRAVEL = "Travel & Places"
    ACTIVITIES = "Activities"
    OBJECTS = "Objects"
    SYMBOLS = "Symbols"
    FLAGS = "Flags"

@dataclass(slots=True)
class Emoji:
    char: str
    name: str
    shortcode: str
    category: str
    aliases: List[str]
    code_point: str

class EmojiDatabase:
    _by_char: Dict[str, Emoji] = {}
    _by_shortcode: Dict[str, Emoji] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        if cls._initialized:
            return
        for start, end in EMOJI_RANGES:
            for codepoint in range(start, end + 1):
                try:
                    char = chr(codepoint)
                    raw_name = unicodedata.name(char)
                except ValueError:
                    continue
                
                name = raw_name.lower().replace("_", " ").replace("-", " ")
                shortcode = f":{raw_name.lower().replace(' ', '_').replace('-', '_')}:"
                category = cls._classify(raw_name)
                cp_str = f"U+{codepoint:X}"
                
                aliases = [raw_name.lower()]
                if "face" in name:
                    aliases.append(name.replace("face", "").strip())
                    
                emoji_obj = Emoji(
                    char=char,
                    name=name,
                    shortcode=shortcode,
                    category=category,
                    aliases=aliases,
                    code_point=cp_str
                )
                cls._by_char[char] = emoji_obj
                cls._by_shortcode[shortcode] = emoji_obj
        cls._initialized = True

    @classmethod
    def _classify(cls, raw_name: str) -> str:
        name = raw_name.upper()
        if any(k in name for k in ["FLAG", "REGIONAL INDICATOR"]):
            return EmojiCategory.FLAGS
        if any(k in name for k in ["FACE", "SMILING", "GRINNING", "LAUGHING", "TEARS", "EYES", "HEART", "KISS", "CAT", "EMOTION"]):
            return EmojiCategory.SMILEYS
        if any(k in name for k in ["HAND", "FINGER", "MAN", "WOMAN", "BOY", "GIRL", "PEOPLE", "PERSON", "BABY", "ADULT", "HAIR", "FOOT", "LEG", "EAR", "NOSE"]):
            return EmojiCategory.PEOPLE
        if any(k in name for k in ["FOOD", "DRINK", "FRUIT", "VEGETABLE", "MEAT", "BREAD", "CAKE", "WINE", "BEER", "COFFEE", "TEA", "SWEET", "COOK", "PLATE", "FORK", "SPOON"]):
            return EmojiCategory.FOOD
        if any(k in name for k in ["CAR", "TRAIN", "PLANE", "BOAT", "HOUSE", "BUILDING", "MOUNTAIN", "BEACH", "ISLAND", "MAP", "GLOBE", "SPACE", "ROCKET", "TICKET"]):
            return EmojiCategory.TRAVEL
        if any(k in name for k in ["SPORTS", "GAME", "BALL", "TROPHY", "MEDAL", "MUSIC", "GUITAR", "PIANO", "ART", "PAINT", "MOVIE", "BOOK", "DANCE", "CARD"]):
            return EmojiCategory.ACTIVITIES
        if any(k in name for k in ["CAT", "DOG", "ANIMAL", "BIRD", "FISH", "MONKEY", "HORSE", "BEAR", "PANDA", "FLOWER", "TREE", "LEAF", "PLANT", "EARTH", "SUN", "CLOUD", "RAIN", "SNOW", "FIRE", "WATER", "WIND", "MOON", "STAR"]):
            return EmojiCategory.ANIMALS
        if any(k in name for k in ["PHONE", "COMPUTER", "CLOCK", "WATCH", "BOOK", "PEN", "PENCIL", "PAPER", "MAIL", "ENVELOPE", "BAG", "KEY", "TOOL", "HAMMER", "WEAPON", "SHIELD", "CROWN", "COIN", "MONEY", "GEM", "RING", "BOX", "BED", "DOOR", "CHAIR", "LAMP", "UMBRELLA"]):
            return EmojiCategory.OBJECTS
        return EmojiCategory.SYMBOLS

    @classmethod
    def get(cls, key: str) -> Optional[Emoji]:
        cls.initialize()
        if key in cls._by_char:
            return cls._by_char[key]
        if key in cls._by_shortcode:
            return cls._by_shortcode[key]
        if not key.startswith(":") and f":{key}:" in cls._by_shortcode:
            return cls._by_shortcode[f":{key}:"]
        key_lower = key.lower()
        for emoji in cls._by_char.values():
            if emoji.name == key_lower or emoji.code_point.lower() == key_lower or key_lower in emoji.aliases:
                return emoji
        return None

    @classmethod
    def search(cls, query: str) -> List[Emoji]:
        cls.initialize()
        query_lower = query.lower()
        results = []
        for emoji in cls._by_char.values():
            if query_lower in emoji.name or query_lower in emoji.shortcode or any(query_lower in a for a in emoji.aliases):
                results.append(emoji)
        return results

class EmojiLookup:
    @staticmethod
    def to_emoji(value: str) -> Optional[str]:
        emoji = EmojiDatabase.get(value)
        return emoji.char if emoji else None

    @staticmethod
    def to_shortcode(value: str) -> Optional[str]:
        emoji = EmojiDatabase.get(value)
        return emoji.shortcode if emoji else None

    @staticmethod
    def to_unicode(value: str) -> Optional[str]:
        emoji = EmojiDatabase.get(value)
        return emoji.code_point if emoji else None

class EmojiParser:
    @staticmethod
    def parse(text: str) -> List[Emoji]:
        EmojiDatabase.initialize()
        found = []
        for char in text:
            emoji = EmojiDatabase.get(char)
            if emoji:
                found.append(emoji)
        return found

    @staticmethod
    def replace_shortcodes(text: str) -> str:
        EmojiDatabase.initialize()
        def replace(match):
            shortcode = match.group(0)
            emoji = EmojiDatabase.get(shortcode)
            return emoji.char if emoji else shortcode
        return re.sub(r':[a-z0-9_]+:', replace, text)

class EmojiFormatter:
    @staticmethod
    def demojize(text: str) -> str:
        EmojiDatabase.initialize()
        result = []
        for char in text:
            emoji = EmojiDatabase.get(char)
            if emoji:
                result.append(emoji.shortcode)
            else:
                result.append(char)
        return "".join(result)
