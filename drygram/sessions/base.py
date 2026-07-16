# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from typing import Optional

class BaseSession:
    """
    Abstract base session storage engine.

    Parameters
    ----------
    session_id : str
        Unique identifier for the session.

    Attributes
    ----------
    session_id : str
        Unique session ID.
    dc_id : int
        Target Data Center ID.
    server_address : str
        Target Data Center IP address.
    server_port : int
        Target Data Center TCP port.
    auth_key : Optional[bytes]
        Generated MTProto authorization key.
    user_id : Optional[int]
        Authenticated user identifier.
    is_bot : bool
        True if credentials represent a bot token.
    """

    def __init__(self, session_id: str):
        """Initialize the BaseSession."""
        self.session_id = session_id
        self.dc_id: int = 1
        self.server_address: str = "149.154.167.50"
        self.server_port: int = 443
        self.auth_key: Optional[bytes] = None
        self.user_id: Optional[int] = None
        self.is_bot: bool = False

    async def load(self) -> None:
        """Load session properties from storage."""
        pass

    async def save(self) -> None:
        """Save session properties to storage."""
        pass

    async def delete(self) -> None:
        """Erase session storage properties."""
        pass
