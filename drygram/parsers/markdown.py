# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import re
from typing import List, Tuple, Dict, Any

class MarkdownParser:
    @staticmethod
    def parse(text: str) -> Tuple[str, List[Dict[str, Any]]]:
        entities = []
        
        patterns = [
            ("bold", re.compile(r"\*\*(.*?)\*\*")),
            ("italic", re.compile(r"\*(.*?)\*")),
            ("underline", re.compile(r"__(.*?)__")),
            ("strikethrough", re.compile(r"~~(.*?)~~")),
            ("spoiler", re.compile(r"\|\|(.*?)\|\|")),
            ("code", re.compile(r"`(.*?)`")),
            ("pre", re.compile(r"```([\s\S]*?)```")),
            ("text_link", re.compile(r"\[(.*?)\]\((.*?)\)")),
            ("blockquote", re.compile(r"^>\s*(.*)$", re.MULTILINE))
        ]
        
        current_text = text
        for name, pattern in patterns:
            while True:
                match = pattern.search(current_text)
                if not match:
                    break
                
                start = match.start()
                if name == "text_link":
                    url = match.group(2)
                    match_text = match.group(1)
                    inner_len = len(match_text)
                    
                    if url.startswith("tg://emoji?id="):
                        emoji_id = url.split("=")[-1]
                        entity = {
                            "type": "custom_emoji",
                            "offset": start,
                            "length": inner_len,
                            "custom_emoji_id": emoji_id
                        }
                    else:
                        entity = {
                            "type": "text_link",
                            "offset": start,
                            "length": inner_len,
                            "url": url
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
