# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Any, List, Dict, Optional

class CommandContext:
    """
    Encapsulates client connection references and update state parameters 
    for executing commands.
    """
    def __init__(
        self,
        client: Any,
        message: Any,
        command: Any,
        arguments: List[Any],
        flags: Dict[str, Any]
    ):
        self.client = client
        self.message = message
        self.chat = getattr(message, "chat", None)
        self.user = getattr(message, "sender", None)
        self.sender = getattr(message, "sender", None)
        self.command = command
        self.arguments = arguments
        self.flags = flags
        self.reply = getattr(message, "reply_to_message_id", None)
        self.entities = getattr(message, "entities", [])
        self.media = getattr(message, "media", None)
        self.session = getattr(client, "session", None)
        self.raw = getattr(client, "raw", None)
        self.dispatcher = getattr(client, "dispatcher", None)
        self.network = getattr(client, "network", None)
        self.storage = getattr(client, "storage", None)

    async def respond(self, text: str, **kwargs) -> Any:
        """Reply to the message that triggered this command."""
        return await self.client.echo(self.message, text, **kwargs)
