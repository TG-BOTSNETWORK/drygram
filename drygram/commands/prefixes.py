# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import List, Dict, Callable, Any, Optional

class PrefixManager:
    """
    Manages and resolves command prefixes globally, dynamically, and per context.
    """
    def __init__(self, default_prefixes: Optional[List[str]] = None):
        self.global_prefixes = default_prefixes or ["/", "!", "."]
        self.chat_prefixes: Dict[int, List[str]] = {}
        self.user_prefixes: Dict[int, List[str]] = {}
        self.plugin_prefixes: Dict[str, List[str]] = {}
        self.dynamic_resolver: Optional[Callable[[Any, Any], List[str]]] = None

    def resolve(self, client: Any, message: Any) -> List[str]:
        """Resolve valid prefixes for the current message context."""
        if self.dynamic_resolver:
            try:
                res = self.dynamic_resolver(client, message)
                if res is not None:
                    return res
            except Exception:
                pass
        
        chat_id = getattr(message.chat, "id", None)
        if chat_id in self.chat_prefixes:
            return self.chat_prefixes[chat_id]
            
        user_id = getattr(message.sender, "id", None)
        if user_id in self.user_prefixes:
            return self.user_prefixes[user_id]
            
        return self.global_prefixes

    def set_chat_prefixes(self, chat_id: int, prefixes: List[str]) -> None:
        """Set prefixes for a specific chat."""
        self.chat_prefixes[chat_id] = prefixes

    def set_user_prefixes(self, user_id: int, prefixes: List[str]) -> None:
        """Set prefixes for a specific user."""
        self.user_prefixes[user_id] = prefixes

    def set_plugin_prefixes(self, plugin_name: str, prefixes: List[str]) -> None:
        """Set prefixes for a specific plugin namespace."""
        self.plugin_prefixes[plugin_name] = prefixes

    def register_resolver(self, resolver: Callable[[Any, Any], List[str]]) -> None:
        """Register a dynamic prefix resolver callback."""
        self.dynamic_resolver = resolver
