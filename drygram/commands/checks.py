# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import inspect
from typing import Any, Callable

class Check:
    """
    Encapsulates custom verification preconditions for commands.
    """
    def __init__(self, callback: Callable[[Any], bool]):
        self.callback = callback

    async def run(self, context: Any) -> bool:
        """Execute the check validation callback."""
        try:
            if inspect.iscoroutinefunction(self.callback):
                return await self.callback(context)
            return self.callback(context)
        except Exception:
            return False
