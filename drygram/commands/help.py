# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Any, List
from drygram.commands.registry import CommandRegistry

class CommandHelp:
    """
    Auto-generates contextual documentation and help descriptions for commands.
    """
    @staticmethod
    def generate_global_help(registry: CommandRegistry, prefixes: List[str]) -> str:
        """Create a master directory of all registered categories and commands."""
        prefix = prefixes[0] if prefixes else "/"
        lines = ["**Available Commands:**\n"]
        for cat_name, cat in registry.categories.items():
            lines.append(f"__Category: {cat_name}__")
            for cmd in cat.commands:
                aliases_str = f" (aliases: {', '.join(cmd.aliases)})" if cmd.aliases else ""
                lines.append(f"• `{prefix}{cmd.name}`{aliases_str} - {cmd.description or 'No description'}")
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def generate_command_help(cmd: Any, prefix: str) -> str:
        """Create target usage guide for a single command."""
        lines = [
            f"**Command:** `{prefix}{cmd.name}`",
            f"**Description:** {cmd.description or 'No description'}"
        ]
        if cmd.aliases:
            lines.append(f"**Aliases:** {', '.join(cmd.aliases)}")
        
        requirements = []
        if cmd.permissions.owner_only: requirements.append("Owner Only")
        if cmd.permissions.admin_only: requirements.append("Admin Only")
        if cmd.permissions.premium_only: requirements.append("Premium Only")
        if cmd.permissions.business_only: requirements.append("Business Only")
        if cmd.permissions.private_only: requirements.append("Private Chats Only")
        if cmd.permissions.group_only: requirements.append("Groups Only")
        if cmd.permissions.channel_only: requirements.append("Channels Only")
        if cmd.permissions.topic_only: requirements.append("Topics Only")
        
        if requirements:
            lines.append(f"**Requirements:** {', '.join(requirements)}")
            
        if cmd.cooldown:
            lines.append(f"**Cooldown:** {cmd.cooldown.rate} call(s) per {cmd.cooldown.per}s")
            
        return "\n".join(lines)

class CommandHelpGenerator:
    @staticmethod
    def generate(name: str, cmd: Any) -> str:
        """Compatibility wrapper to generate command help text."""
        return CommandHelp.generate_command_help(cmd, "/")
