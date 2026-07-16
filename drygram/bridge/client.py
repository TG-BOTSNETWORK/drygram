# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from typing import Any, Optional, Union
from drygram.client import DryClient

class BridgeClient(DryClient):
    """
    Bridge client wrapping DryClient to provide compatibility for external voice libraries.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def reconnect(self) -> None:
        """Helper to reconnect the client network pool."""
        await self.restart()

    async def synchronize_updates(self) -> None:
        """Helper to synchronize update streams."""
        if self.dispatcher:
            # Re-starts the update processor pipeline
            await self.dispatcher.stop()
            await self.dispatcher.start()
