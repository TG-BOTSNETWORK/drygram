# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import redis.asyncio as redis
from typing import Optional
from drygram.sessions.base import BaseSession

class RedisSession(BaseSession):
    """
    Redis based remote session storage engine.

    Parameters
    ----------
    session_id : str
        Unique identifier for the session.
    redis_url : str
        Target Redis URL scheme (e.g. redis://127.0.0.1:6379/0).

    Attributes
    ----------
    redis_url : str
        Target connection URL.
    """

    def __init__(self, session_id: str, redis_url: str):
        """
        Initialize the RedisSession.

        Parameters
        ----------
        session_id : str
            Unique session ID.
        redis_url : str
            Redis connection URL.
        """
        super().__init__(session_id)
        self.redis_url = redis_url

    async def load(self) -> None:
        """Load session properties from Redis hash key."""
        client = redis.from_url(self.redis_url)
        try:
            key = f"drygram_session:{self.session_id}"
            data = await client.hgetall(key)
            if data:
                self.dc_id = int(data.get(b"dc_id", b"1"))
                self.server_address = data.get(b"server_address", b"149.154.167.50").decode()
                self.server_port = int(data.get(b"server_port", b"443"))
                self.auth_key = data.get(b"auth_key")
                user_id_raw = data.get(b"user_id")
                self.user_id = int(user_id_raw) if user_id_raw else None
                self.is_bot = data.get(b"is_bot") == b"1"
        finally:
            await client.aclose()

    async def save(self) -> None:
        """Save session properties to Redis hash key."""
        client = redis.from_url(self.redis_url)
        try:
            key = f"drygram_session:{self.session_id}"
            mapping = {
                "dc_id": str(self.dc_id),
                "server_address": self.server_address,
                "server_port": str(self.server_port),
                "is_bot": "1" if self.is_bot else "0"
            }
            if self.auth_key:
                mapping["auth_key"] = self.auth_key
            if self.user_id:
                mapping["user_id"] = str(self.user_id)
            await client.hset(key, mapping=mapping)
        finally:
            await client.aclose()

    async def delete(self) -> None:
        """Erase the current session record from Redis."""
        client = redis.from_url(self.redis_url)
        try:
            key = f"drygram_session:{self.session_id}"
            await client.delete(key)
        finally:
            await client.aclose()
        self.auth_key = None
        self.user_id = None
        self.is_bot = False
