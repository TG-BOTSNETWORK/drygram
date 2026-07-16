# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import List, Any

class CommandCategory:
    """
    Groups registered commands by topic or category (e.g. Admin, Fun, Utility).
    """
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.commands: List[Any] = []
