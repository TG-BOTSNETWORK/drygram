# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

"""
Encrypted Session Storage Backend.
"""

import os
import hashlib
from typing import Optional, Union
from drygram.sessions.session import Session
from drygram.errors.rpc import SessionError

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    AESGCM = None


class EncryptedSession(Session):
    """
    Saves/loads session state as an encrypted binary file on disk.
    """

    def __init__(self, session_id: str, encryption_key: Union[str, bytes], filepath: Optional[str] = None):
        super().__init__(session_id)
        self.encryption_key = encryption_key
        self.filepath = filepath or f"{session_id}.enc"

    def _get_key(self) -> bytes:
        """Derive 32-byte key from password/key."""
        if isinstance(self.encryption_key, str):
            return hashlib.sha256(self.encryption_key.encode("utf-8")).digest()
        return hashlib.sha256(self.encryption_key).digest()

    async def load(self) -> None:
        """Load and decrypt session fields from file."""
        if not os.path.exists(self.filepath):
            return

        if not AESGCM:
            raise SessionError("cryptography library not installed or AESGCM not supported")

        try:
            with open(self.filepath, "rb") as f:
                raw_bytes = f.read()

            if len(raw_bytes) < 12:
                raise SessionError("Encrypted session file is corrupted")

            nonce = raw_bytes[:12]
            ciphertext = raw_bytes[12:]
            
            key = self._get_key()
            aesgcm = AESGCM(key)
            full_block = aesgcm.decrypt(nonce, ciphertext, b"drygram_encrypted_session")

            if len(full_block) < 8:
                raise SessionError("Decrypted block too small")

            checksum = full_block[:8]
            payload = full_block[8:]

            # Verify checksum
            checksum_calc = hashlib.sha256(payload).digest()[:8]
            if checksum != checksum_calc:
                raise SessionError("Decrypted session integrity check failed")

            fields, _ = self._deserialize_payload(payload)
            for k, v in fields.items():
                setattr(self, k, v)
        except Exception as e:
            raise SessionError(f"Failed to load encrypted session: {str(e)}")

    async def save(self) -> None:
        """Encrypt and save session fields to file."""
        if not AESGCM:
            raise SessionError("cryptography library not installed or AESGCM not supported")

        try:
            payload = self._serialize_payload()
            chk = self.checksum
            full_block = chk + payload

            key = self._get_key()
            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, full_block, b"drygram_encrypted_session")
            encrypted_payload = nonce + ciphertext

            with open(self.filepath, "wb") as f:
                f.write(encrypted_payload)
        except Exception as e:
            raise SessionError(f"Failed to save encrypted session: {str(e)}")

    async def delete(self) -> None:
        """Delete the encrypted session file."""
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
