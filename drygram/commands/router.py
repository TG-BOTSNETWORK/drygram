# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import logging
from typing import Any, Optional, List
from drygram.commands.registry import CommandRegistry
from drygram.commands.prefixes import PrefixManager
from drygram.commands.matcher import CommandMatcher
from drygram.commands.parser import CommandParser
from drygram.commands.context import CommandContext
from drygram.commands.executor import CommandExecutor
from drygram.commands.history import CommandHistory
from drygram.commands.analytics import CommandAnalytics
from drygram.commands.help import CommandHelp

logger = logging.getLogger(__name__)

class CommandRouter:
    """
    Hooks into dispatcher update loop, parses commands/subcommands, and triggers executor.
    """
    def __init__(self, registry: Optional[Any] = None, client: Optional[Any] = None):
        if isinstance(registry, CommandRegistry):
            self.registry = registry
            self.client = client
        else:
            self.client = registry
            from drygram.commands.decorators import _global_registry
            self.registry = client or _global_registry

        self.prefixes = PrefixManager()
        from drygram.commands.history import _global_history
        self.history = _global_history
        self.analytics = CommandAnalytics(self.history)
        
        if self.client:
            from drygram.dispatch.watcher import Watcher
            from drygram.dispatch.gate import Gates
            # Listen for any text message signals in the update pipeline
            watcher = Watcher(self._route_message, gate=Gates.all_signals(), group=0)
            self.client.dispatcher.add_watcher(watcher)

    async def route(self, client: Any, message: Any) -> bool:
        """Route and execute a command from a raw message."""
        text = getattr(message, "text", None)
        if not text:
            return False
            
        prefixes = self.prefixes.resolve(client, message)
        match = CommandMatcher.match_trigger(text, prefixes)
        if not match:
            return False
            
        cmd_name, args_text = match
        cmd = self.registry.get(cmd_name)
        if not cmd:
            return False
            
        args, flags = CommandParser.parse(args_text)
        ctx = CommandContext(client, message, cmd, args, flags)
        await CommandExecutor.execute(ctx)
        return True

    async def _route_message(self, message: Any) -> None:
        text = getattr(message, "text", None)
        if not text:
            return
            
        prefixes = self.prefixes.resolve(self.client, message)
        match = CommandMatcher.match_trigger(text, prefixes)
        if not match:
            return
            
        cmd_name, args_text = match
        cmd_name_lower = cmd_name.lower()
        
        # Support automatic help command
        if cmd_name_lower == "help":
            if args_text:
                target_cmd_name = args_text.strip().lower()
                if target_cmd_name in self.registry.commands:
                    cmd = self.registry.commands[target_cmd_name]
                    prefix = prefixes[0] if prefixes else "/"
                    help_text = CommandHelp.generate_command_help(cmd, prefix)
                    await self.client.echo(message, help_text)
                    return
            help_text = CommandHelp.generate_global_help(self.registry, prefixes)
            await self.client.echo(message, help_text)
            return

        # Check if match is a group namespace
        if cmd_name_lower in self.registry.groups:
            group = self.registry.groups[cmd_name_lower]
            sub_parts = args_text.split(maxsplit=1)
            if sub_parts:
                sub_name = sub_parts[0].lower()
                sub_args_text = sub_parts[1] if len(sub_parts) > 1 else ""
                if sub_name in group.commands:
                    cmd = group.commands[sub_name]
                    await self._dispatch_command(cmd, message, sub_args_text)
                    return

        # Check if match is a direct command
        if cmd_name_lower in self.registry.commands:
            cmd = self.registry.commands[cmd_name_lower]
            await self._dispatch_command(cmd, message, args_text)

    async def _dispatch_command(self, cmd: Any, message: Any, args_text: str) -> None:
        from drygram.commands.context import CommandContext
        temp_ctx = CommandContext(self.client, message, cmd, [], {})
        
        if not cmd.permissions.check(temp_ctx):
            self.history.log_call(cmd.name, getattr(message.sender, "id", None), getattr(message.chat, "id", None), False, "Permissions Denied")
            await self.client.echo(message, "Error: Permissions verification failed.")
            return

        if cmd.cooldown:
            key = getattr(message.sender, "id", 0)
            is_limited, remaining = cmd.cooldown.check_cooldown(key)
            if is_limited:
                self.history.log_call(cmd.name, getattr(message.sender, "id", None), getattr(message.chat, "id", None), False, "Cooldown Active")
                await self.client.echo(message, f"Error: Command rate limited. Please wait {remaining:.1f}s.")
                return
            cmd.cooldown.update_cooldown(key)

        args, flags = CommandParser.parse(args_text)
        ctx = CommandContext(self.client, message, cmd, args, flags)

        try:
            await CommandExecutor.execute(ctx)
            self.history.log_call(cmd.name, getattr(message.sender, "id", None), getattr(message.chat, "id", None), True)
        except Exception as e:
            self.history.log_call(cmd.name, getattr(message.sender, "id", None), getattr(message.chat, "id", None), False, str(e))
            await self.client.echo(message, f"Error: {str(e)}")
