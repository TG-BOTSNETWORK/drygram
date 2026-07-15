# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import re
from typing import List, Tuple, Dict, Any

class HTMLParser:
    @staticmethod
    def parse(text: str) -> Tuple[str, List[Dict[str, Any]]]:
        entities = []
        patterns = [
            ("bold", re.compile(r"<(?:b|strong)>(.*?)</(?:b|strong)>", re.DOTALL)),
            ("italic", re.compile(r"<(?:i|em)>(.*?)</(?:i|em)>", re.DOTALL)),
            ("underline", re.compile(r"<u>(.*?)</u>", re.DOTALL)),
            ("strikethrough", re.compile(r"<(?:s|strike|del)>(.*?)</(?:s|strike|del)>", re.DOTALL)),
            ("spoiler", re.compile(r"<(?:tg-spoiler|spoiler)>(.*?)</(?:tg-spoiler|spoiler)>", re.DOTALL)),
            ("code", re.compile(r"<code>(.*?)</code>", re.DOTALL)),
            ("pre", re.compile(r"<pre>(.*?)</pre>", re.DOTALL)),
            ("blockquote", re.compile(r"<blockquote>(.*?)</blockquote>", re.DOTALL)),
            ("text_link", re.compile(r'<a\s+href="([^"]+)"\s*>(.*?)</a>', re.DOTALL)),
            ("custom_emoji", re.compile(r'<tg-emoji\s+emoji-id="([^"]+)"\s*>(.*?)</tg-emoji>', re.DOTALL))
        ]
        
        current_text = text
        for name, pattern in patterns:
            while True:
                match = pattern.search(current_text)
                if not match:
                    break
                
                start = match.start()
                if name == "text_link":
                    url = match.group(1)
                    match_text = match.group(2)
                    inner_len = len(match_text)
                    entity = {
                        "type": "text_link",
                        "offset": start,
                        "length": inner_len,
                        "url": url
                    }
                elif name == "custom_emoji":
                    emoji_id = match.group(1)
                    match_text = match.group(2)
                    inner_len = len(match_text)
                    entity = {
                        "type": "custom_emoji",
                        "offset": start,
                        "length": inner_len,
                        "custom_emoji_id": emoji_id
                    }
                else:
                    match_text = match.group(1)
                    inner_len = len(match_text)
                    entity = {
                        "type": name,
                        "offset": start,
                        "length": inner_len
                    }
                
                current_text = current_text[:start] + match_text + current_text[match.end():]
                
                for ent in entities:
                    if ent["offset"] >= start:
                        ent["offset"] -= (match.end() - start - inner_len)
                        
                entities.append(entity)
                
        mention_patterns = [
            ("mention", re.compile(r"@(\w+)")),
            ("url", re.compile(r"https?://[^\s]+"))
        ]
        for name, pat in mention_patterns:
            for match in pat.finditer(current_text):
                entities.append({
                    "type": name,
                    "offset": match.start(),
                    "length": len(match.group(0))
                })
                
        return current_text, entities
