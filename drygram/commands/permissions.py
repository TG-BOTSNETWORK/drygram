# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Any

class CommandPermission:
    """
    Defines the permission and chat context criteria required for command execution.
    """
    def __init__(
        self,
        owner_only: bool = False,
        admin_only: bool = False,
        premium_only: bool = False,
        business_only: bool = False,
        private_only: bool = False,
        group_only: bool = False,
        channel_only: bool = False,
        topic_only: bool = False
    ):
        self.owner_only = owner_only
        self.admin_only = admin_only
        self.premium_only = premium_only
        self.business_only = business_only
        self.private_only = private_only
        self.group_only = group_only
        self.channel_only = channel_only
        self.topic_only = topic_only

    def check(self, context: Any) -> bool:
        """Check if context matches all declared permissions."""
        user = context.user
        chat = context.chat
        
        if self.private_only and getattr(chat, "type", None) != "private":
            return False
        if self.group_only and getattr(chat, "type", None) not in ("group", "supergroup"):
            return False
        if self.channel_only and getattr(chat, "type", None) != "channel":
            return False
        if self.topic_only and not getattr(context.message, "topic_id", None):
            return False
            
        if self.owner_only:
            # Mock owner checking: ID 12345678 or similar
            if not user or user.id != 12345678:
                return False
                
        if self.admin_only:
            # Mock admin check (user is admin in chat)
            if not user or not chat or chat.type == "private":
                return False
                
        if self.premium_only:
            # Check user.is_premium if available
            if not user or not getattr(user, "is_premium", False):
                return False
                
        if self.business_only:
            if not user or not getattr(user, "is_business", False):
                return False
                
        return True
