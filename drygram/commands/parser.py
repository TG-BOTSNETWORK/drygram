# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import shlex
from typing import List, Tuple, Dict, Any

class CommandParser:
    """
    Parses command input text into positional arguments and keyword flags.
    Supports nested quotes, escape characters, and standard CLI flag notations.
    """
    @staticmethod
    def parse(text: str) -> Tuple[List[str], Dict[str, Any]]:
        if not text:
            return [], {}
            
        try:
            # shlex natively handles escaped characters and nested quotes
            tokens = shlex.split(text)
        except ValueError:
            # Graceful fallback for unbalanced quotes
            tokens = text.split()

        args = []
        flags = {}
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("--"):
                name = token[2:]
                if i + 1 < len(tokens) and not tokens[i+1].startswith("-"):
                    flags[name] = tokens[i+1]
                    i += 2
                else:
                    flags[name] = True
                    i += 1
            elif token.startswith("-") and len(token) > 1:
                name = token[1:]
                if i + 1 < len(tokens) and not tokens[i+1].startswith("-"):
                    flags[name] = tokens[i+1]
                    i += 2
                else:
                    flags[name] = True
                    i += 1
            else:
                args.append(token)
                i += 1
        return args, flags
