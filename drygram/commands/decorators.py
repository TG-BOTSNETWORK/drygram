# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Callable, Optional, List, Any
from drygram.commands.registry import CommandRegistry, Command
from drygram.commands.permissions import CommandPermission
from drygram.commands.cooldown import CooldownManager

# Global registry for decorators
_global_registry = CommandRegistry()

def command(
    name: str,
    aliases: Optional[List[str]] = None,
    description: str = "",
    category: str = "General",
    owner_only: bool = False,
    admin_only: bool = False,
    premium_only: bool = False,
    business_only: bool = False,
    private_only: bool = False,
    group_only: bool = False,
    channel_only: bool = False,
    topic_only: bool = False,
    cooldown_rate: int = 1,
    cooldown_per: float = 0.0
) -> Any:
    """Decorator to register a function as a command."""
    def decorator(func: Any) -> Any:
        perms = CommandPermission(
            owner_only=owner_only,
            admin_only=admin_only,
            premium_only=premium_only,
            business_only=business_only,
            private_only=private_only,
            group_only=group_only,
            channel_only=channel_only,
            topic_only=topic_only
        )
        cd = CooldownManager(rate=cooldown_rate, per=cooldown_per) if cooldown_per > 0 else None
        cmd = Command(
            name=name,
            callback=func,
            aliases=aliases,
            description=description,
            category=category,
            permissions=perms,
            cooldown=cd
        )
        _global_registry.register_command(cmd)
        return func
    return decorator

# Alias decorators representing the command framework API
def observe(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def listen(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def capture(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def watch(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def route(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def respond(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def trigger(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def bind(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
def register(name: str, **kwargs: Any) -> Any: return command(name, **kwargs)
