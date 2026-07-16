# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from drygram.sessions.session import Session

class MemorySession(Session):
    """
    In-memory transient session storage engine.
    """

    async def load(self) -> None:
        """Load session properties (noop for MemorySession)."""
        pass

    async def save(self) -> None:
        """Save session properties (noop for MemorySession)."""
        pass

    async def delete(self) -> None:
        """Erase memory session properties."""
        self.auth_key = None
        self.user_id = None
        self.is_bot = False
