# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Any
from drygram.bridge.client import BridgeClient

class BridgeAdapter:
    """
    Adapter class assisting external voice libraries in interfacing with DryClient/BridgeClient.
    """
    def __init__(self, client: BridgeClient):
        self.client = client

    @property
    def mtproto(self):
        """Access the underlying MTProto engine."""
        return self.client.mtproto

    @property
    def session(self):
        """Access the current session instance."""
        return self.client.session

    @property
    def loop(self):
        """Access the asyncio event loop."""
        return self.client.loop

    @property
    def dispatcher(self):
        """Access the update dispatcher."""
        return self.client.dispatcher

    @property
    def network(self):
        """Access the network layer."""
        return self.client.network

    async def invoke(self, query: Any) -> Any:
        """Send a raw MTProto TL request."""
        return await self.client.invoke(query)

    async def export_session(self) -> str:
        """Export the active session as a serialized string."""
        return await self.client.export_session()

    async def reconnect(self) -> None:
        """Helper to trigger network reconnection."""
        await self.client.reconnect()

    async def synchronize_updates(self) -> None:
        """Helper to synchronize update streams."""
        await self.client.synchronize_updates()
