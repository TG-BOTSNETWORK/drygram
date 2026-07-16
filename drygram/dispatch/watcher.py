# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from typing import Callable, Any, Optional
from drygram.dispatch.gate import Gate

class Watcher:
    """
    Representation of registered update event watchers.

    Parameters
    ----------
    callback : Callable[[Any], Any]
        Handler function invoked on validation.
    gate : Optional[Gate], default=None
        Conditional filter to check before execution.
    group : int, default=0
        Watcher priority group.

    Attributes
    ----------
    callback : Callable[[Any], Any]
        Target callback.
    gate : Optional[Gate]
        Conditional filter.
    group : int
        Priority group.
    """

    def __init__(self, callback: Callable[[Any], Any], gate: Optional[Gate] = None, group: int = 0):
        """
        Initialize the Watcher.

        Parameters
        ----------
        callback : Callable[[Any], Any]
            Execution handler callback.
        gate : Optional[Gate], default=None
            Filter gate logic.
        group : int, default=0
            Priority group.
        """
        self.callback = callback
        self.gate = gate
        self.group = group

    async def execute(self, event: Any) -> bool:
        """
        Execute the handler if filter gate rule resolves.

        Parameters
        ----------
        event : Any
            Target signal update payload.

        Returns
        -------
        bool
            True if callback was executed successfully.
        """
        if self.gate is not None and not self.gate(event):
            return False
        
        if asyncio.iscoroutinefunction(self.callback):
            await self.callback(event)
        else:
            self.callback(event)
        return True
