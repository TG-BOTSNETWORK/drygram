# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Dict, Any

class CommandGroup:
    """
    Groups subcommands under a main namespaces (e.g., config set, config get).
    """
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.commands: Dict[str, Any] = {}

    def command(self, name: str, **kwargs) -> Any:
        """Register a subcommand within the group."""
        def decorator(func: Any) -> Any:
            from drygram.commands.registry import Command
            cmd = Command(name, func, parent_group=self, **kwargs)
            self.commands[name] = cmd
            return func
        return decorator
