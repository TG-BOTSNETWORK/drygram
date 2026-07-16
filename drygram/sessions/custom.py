# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

"""
Custom Session Storage Backend.
"""

from typing import Optional, Callable, Awaitable
from drygram.sessions.session import Session


class CustomSession(Session):
    """
    Delegates session load/save/delete operations to user-supplied asynchronous callback functions.
    """

    def __init__(
        self,
        session_id: str,
        load_callback: Optional[Callable[["CustomSession"], Awaitable[None]]] = None,
        save_callback: Optional[Callable[["CustomSession"], Awaitable[None]]] = None,
        delete_callback: Optional[Callable[["CustomSession"], Awaitable[None]]] = None
    ):
        super().__init__(session_id)
        self.load_callback = load_callback
        self.save_callback = save_callback
        self.delete_callback = delete_callback

    async def load(self) -> None:
        """Call the custom async load handler if provided."""
        if self.load_callback:
            await self.load_callback(self)

    async def save(self) -> None:
        """Call the custom async save handler if provided."""
        if self.save_callback:
            await self.save_callback(self)

    async def delete(self) -> None:
        """Call the custom async delete handler if provided."""
        if self.delete_callback:
            await self.delete_callback(self)
        await self.deauthorize()
