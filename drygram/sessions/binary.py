# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

"""
Binary Session Storage Backend.
"""

import os
from typing import Optional
from drygram.sessions.session import Session
from drygram.errors.rpc import SessionError


class BinarySession(Session):
    """
    Saves/loads session state as a raw binary file on disk.
    """

    def __init__(self, session_id: str, filepath: Optional[str] = None):
        super().__init__(session_id)
        self.filepath = filepath or f"{session_id}.bin"

    async def load(self) -> None:
        """Load session fields from binary file."""
        if not os.path.exists(self.filepath):
            return
        
        try:
            with open(self.filepath, "rb") as f:
                full_block = f.read()
            if len(full_block) < 8:
                raise SessionError("Binary session file too small")
            
            checksum = full_block[:8]
            payload = full_block[8:]
            
            # Reconstruct session fields
            fields, _ = self._deserialize_payload(payload)
            for k, v in fields.items():
                setattr(self, k, v)
        except Exception as e:
            raise SessionError(f"Failed to load binary session: {str(e)}")

    async def save(self) -> None:
        """Save session fields to binary file."""
        try:
            payload = self._serialize_payload()
            chk = self.checksum
            full_block = chk + payload
            with open(self.filepath, "wb") as f:
                f.write(full_block)
        except Exception as e:
            raise SessionError(f"Failed to save binary session: {str(e)}")

    async def delete(self) -> None:
        """Delete the binary session file."""
        if os.path.exists(self.filepath):
            try:
                os.remove(self.filepath)
            except Exception:
                pass
        self.auth_key = None
        self.auth_key_id = None
        self.user_id = None
        self.bot_id = None
        self.auth_state = "destroyed"
