# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Dict

class AliasManager:
    """
    Manages lookup map between short aliases and their target command names.
    """
    def __init__(self):
        self.alias_map: Dict[str, str] = {}
        self.aliases_map = self.alias_map

    def register_alias(self, alias: str, target: str) -> None:
        """Register an alias pointing to a command name."""
        self.alias_map[alias.lower()] = target.lower()

    def resolve_alias(self, name: str) -> str:
        """Resolve alias name to target command name."""
        return self.alias_map.get(name.lower(), name.lower())

    def add_alias(self, alias: str, target: str) -> None:
        """Compatibility wrapper to register an alias."""
        self.register_alias(alias, target)

CommandAliases = AliasManager
