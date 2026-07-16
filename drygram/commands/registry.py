# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import List, Callable, Optional, Dict, Any
from drygram.commands.permissions import CommandPermission
from drygram.commands.cooldown import CooldownManager

class Command:
    """
    Holds metadata and callback handlers for individual commands.
    """
    def __init__(
        self,
        name: str,
        callback: Callable[..., Any],
        aliases: Optional[List[str]] = None,
        description: str = "",
        category: str = "General",
        permissions: Optional[CommandPermission] = None,
        cooldown: Optional[CooldownManager] = None,
        parent_group: Optional[Any] = None,
        args: Optional[List[Any]] = None
    ):
        self.name = name
        self.callback = callback
        self.aliases = aliases or []
        self.description = description
        self.category = category
        self.permissions = permissions or CommandPermission()
        self.cooldown = cooldown
        self.parent_group = parent_group
        self.args = args or []

class CommandRegistry:
    """
    Database of active commands, subcommands, aliases, and categories.
    """
    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self.groups: Dict[str, Any] = {}
        self.categories: Dict[str, Any] = {}

    def register_command(self, cmd: Command) -> None:
        """Register a command in the global registry."""
        self.commands[cmd.name.lower()] = cmd
        for alias in cmd.aliases:
            self.commands[alias.lower()] = cmd
            
        from drygram.commands.categories import CommandCategory
        cat_name = cmd.category
        if cat_name not in self.categories:
            self.categories[cat_name] = CommandCategory(cat_name)
        self.categories[cat_name].commands.append(cmd)

    def register_group(self, group: Any) -> None:
        """Register a command group."""
        self.groups[group.name.lower()] = group

    def register(
        self,
        name: str,
        callback: Any,
        args: Optional[List[Any]] = None,
        permissions: Optional[List[str]] = None,
        cooldown: float = 0.0,
        category: str = "General",
        description: str = ""
    ) -> None:
        """Register a command using legacy compatibility parameters."""
        owner_only = "owner" in (permissions or [])
        admin_only = "admin" in (permissions or [])
        perms = CommandPermission(owner_only=owner_only, admin_only=admin_only)
        
        cd = CooldownManager(rate=1, per=cooldown) if cooldown > 0 else None
        
        cmd = Command(
            name=name,
            callback=callback,
            description=description,
            category=category,
            permissions=perms,
            cooldown=cd,
            args=args
        )
        self.register_command(cmd)

    def get(self, name: str) -> Optional[Command]:
        """Retrieve a command by name."""
        return self.commands.get(name.lower())
