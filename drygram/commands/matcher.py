# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Optional, List, Tuple

class CommandMatcher:
    """
    Identifies if a message text is a command call based on configured prefixes.
    """
    @staticmethod
    def match_trigger(text: str, prefixes: List[str]) -> Optional[Tuple[str, str]]:
        """
        Checks if text matches any prefix.
        Returns:
            (command_name, arguments_text) or None
        """
        if not text:
            return None
            
        for prefix in prefixes:
            if text.startswith(prefix):
                rest = text[len(prefix):].strip()
                if not rest:
                    continue
                parts = rest.split(maxsplit=1)
                cmd_name = parts[0]
                args_text = parts[1] if len(parts) > 1 else ""
                return cmd_name, args_text
                
        return None

    @staticmethod
    def is_match(text: str, cmd_name: str) -> bool:
        """Compatibility helper to verify if a text is a command trigger match."""
        if not text:
            return False
        for prefix in ["/", "!", "."]:
            if text.startswith(prefix + cmd_name):
                return True
        return False
