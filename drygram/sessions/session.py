# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

"""
DryGram Dedicated Session Core.

This module contains the primary Session base class containing all session metadata
required for Telegram MTProto client, custom serialization to/from DryGram Session String,
and core session lifecycle operations.
"""

import time
import struct
import base64
import json
import os
import hashlib
from typing import Optional, Union, Any, Tuple
from drygram.sessions.base import BaseSession
from drygram.errors.rpc import SessionError, AuthError

# Try importing cryptography primitives for session string encryption
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    AESGCM = None


class Session(BaseSession):
    """
    Dedicated Session class representing MTProto state and connection metadata.
    Inherits from BaseSession for compatibility.
    """

    def __init__(self, session_id: str):
        super().__init__(session_id)
        # Session parameters and credentials
        self.auth_key: Optional[bytes] = None
        self.auth_key_id: Optional[int] = None
        self.server_salt: int = 0
        self.api_id: int = 0
        self.test_mode: bool = False
        self.layer: int = 184
        self.device_model: str = "Unknown Device"
        self.system_version: str = "Unknown System"
        self.app_version: str = "1.0.0"
        self.lang_code: str = "en"
        self.system_lang_code: str = "en"
        self.proxy: Optional[dict] = None
        self.ipv6: bool = False
        self.created_at: int = int(time.time())
        self.updated_at: int = int(time.time())
        self.last_connected: int = 0
        self.takeout_id: Optional[int] = None
        self.bot_id: Optional[int] = None
        self.phone_number: Optional[str] = None
        self.username: Optional[str] = None
        self.connection_mode: str = "tcp"
        self.transport_type: str = "intermediate"
        self.auth_state: str = "unauthorized"

    @property
    def version(self) -> int:
        """Get the serialization protocol version of this session."""
        return 1

    @property
    def checksum(self) -> bytes:
        """Compute SHA256 checksum of the current session data state."""
        raw = self._serialize_payload()
        return hashlib.sha256(raw).digest()[:8]

    def validate(self) -> bool:
        """
        Verify that the session data integrity is correct and essential values exist.

        Returns
        -------
        bool
            True if session is valid.
        """
        if not self.session_id:
            return False
        if not self.dc_id or not (1 <= self.dc_id <= 5):
            return False
        if self.auth_key and len(self.auth_key) != 256:
            return False
        return True

    def is_valid(self) -> bool:
        """
        Check if the session has a valid authorization key.

        Returns
        -------
        bool
            True if authorized.
        """
        return self.validate() and self.auth_key is not None

    def _serialize_payload(self) -> bytes:
        """Serialize session properties into a binary payload."""
        # 1. Primitives packing
        takeout_val = self.takeout_id if self.takeout_id is not None else -1
        user_val = self.user_id if self.user_id is not None else -1
        bot_val = self.bot_id if self.bot_id is not None else -1
        auth_key_id_val = self.auth_key_id if self.auth_key_id is not None else 0

        prim_bytes = struct.pack(
            "<IBH??IQQQqqq?QQ",
            self.api_id,
            self.dc_id,
            self.server_port,
            self.test_mode,
            self.ipv6,
            self.layer,
            self.created_at,
            self.updated_at,
            self.last_connected,
            takeout_val,
            user_val,
            bot_val,
            self.is_bot,
            auth_key_id_val,
            self.server_salt
        )

        # 2. Length-prefixed variable fields helper
        def pack_bytes(b: Optional[bytes]) -> bytes:
            if not b:
                return struct.pack("<H", 0)
            return struct.pack("<H", len(b)) + b

        def pack_str(s: Optional[str]) -> bytes:
            if not s:
                return struct.pack("<H", 0)
            b = s.encode("utf-8")
            return struct.pack("<H", len(b)) + b

        var_parts = [
            pack_bytes(self.auth_key),
            pack_str(self.server_address),
            pack_str(self.session_id),
            pack_str(self.device_model),
            pack_str(self.system_version),
            pack_str(self.app_version),
            pack_str(self.lang_code),
            pack_str(self.system_lang_code),
            pack_str(self.phone_number),
            pack_str(self.username),
            pack_str(self.connection_mode),
            pack_str(self.transport_type),
            pack_str(self.auth_state),
            pack_str(json.dumps(self.proxy) if self.proxy else None)
        ]

        return prim_bytes + b"".join(var_parts)

    @classmethod
    def _deserialize_payload(cls, data: bytes) -> Tuple[dict, int]:
        """Deserialize binary payload back to field dictionary."""
        prim_fmt = "<IBH??IQQQqqq?QQ"
        prim_size = struct.calcsize(prim_fmt)
        if len(data) < prim_size:
            raise ValueError("Binary payload is too short")

        prims = struct.unpack(prim_fmt, data[:prim_size])
        offset = prim_size

        def unpack_bytes() -> Tuple[bytes, int]:
            nonlocal offset
            length = struct.unpack_from("<H", data, offset)[0]
            offset += 2
            val = data[offset:offset+length]
            offset += length
            return val, offset

        def unpack_str() -> Tuple[str, int]:
            b, _ = unpack_bytes()
            return b.decode("utf-8"), offset

        auth_key_raw, _ = unpack_bytes()
        server_address, _ = unpack_str()
        session_id, _ = unpack_str()
        device_model, _ = unpack_str()
        system_version, _ = unpack_str()
        app_version, _ = unpack_str()
        lang_code, _ = unpack_str()
        system_lang_code, _ = unpack_str()
        phone_number, _ = unpack_str()
        username, _ = unpack_str()
        connection_mode, _ = unpack_str()
        transport_type, _ = unpack_str()
        auth_state, _ = unpack_str()
        proxy_str, _ = unpack_str()

        proxy_val = None
        if proxy_str:
            try:
                proxy_val = json.loads(proxy_str)
            except Exception:
                pass

        fields = {
            "api_id": prims[0],
            "dc_id": prims[1],
            "server_port": prims[2],
            "test_mode": prims[3],
            "ipv6": prims[4],
            "layer": prims[5],
            "created_at": prims[6],
            "updated_at": prims[7],
            "last_connected": prims[8],
            "takeout_id": prims[9] if prims[9] != -1 else None,
            "user_id": prims[10] if prims[10] != -1 else None,
            "bot_id": prims[11] if prims[11] != -1 else None,
            "is_bot": prims[12],
            "auth_key_id": prims[13] if prims[13] != 0 else None,
            "server_salt": prims[14],
            "auth_key": auth_key_raw if auth_key_raw else None,
            "server_address": server_address,
            "session_id": session_id,
            "device_model": device_model,
            "system_version": system_version,
            "app_version": app_version,
            "lang_code": lang_code,
            "system_lang_code": system_lang_code,
            "phone_number": phone_number if phone_number else None,
            "username": username if username else None,
            "connection_mode": connection_mode,
            "transport_type": transport_type,
            "auth_state": auth_state,
            "proxy": proxy_val
        }
        return fields, offset

    def to_string(self, encryption_key: Optional[Union[str, bytes]] = None) -> str:
        """
        Serialize this session to a secure, unique DryGram Session String format.

        Parameters
        ----------
        encryption_key : Optional[Union[str, bytes]], default=None
            Optional key/password to encrypt the session string.

        Returns
        -------
        str
            DryGram Session String.
        """
        payload = self._serialize_payload()
        chk = self.checksum
        full_block = chk + payload

        if encryption_key:
            if not AESGCM:
                raise SessionError("cryptography library not installed or AESGCM not supported")
            
            # Derive 32-byte key from password
            if isinstance(encryption_key, str):
                key = hashlib.sha256(encryption_key.encode("utf-8")).digest()
            else:
                key = hashlib.sha256(encryption_key).digest()

            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, full_block, b"drygram_session")
            encrypted_payload = nonce + ciphertext
            b64 = base64.urlsafe_b64encode(encrypted_payload).decode("utf-8").rstrip("=")
            return f"DRY1E_{b64}"
        else:
            b64 = base64.urlsafe_b64encode(full_block).decode("utf-8").rstrip("=")
            return f"DRY1U_{b64}"

    @classmethod
    def from_string(cls, session_string: str, encryption_key: Optional[Union[str, bytes]] = None) -> "Session":
        """
        Deserialize a Session from a DryGram Session String.

        Parameters
        ----------
        session_string : str
            The DryGram Session String.
        encryption_key : Optional[Union[str, bytes]], default=None
            Optional key/password if the session string is encrypted.

        Returns
        -------
        Session
            A newly initialized Session instance.
        """
        if not session_string.startswith("DRY1"):
            raise SessionError("Invalid or unsupported session string format version")

        # Padding recovery
        token = session_string[6:]
        padding_needed = 4 - (len(token) % 4)
        if padding_needed < 4:
            token += "=" * padding_needed

        try:
            raw_bytes = base64.urlsafe_b64decode(token)
        except Exception as e:
            raise SessionError(f"Failed to base64 decode session string: {str(e)}")

        if session_string.startswith("DRY1E_"):
            if not encryption_key:
                raise SessionError("Encryption key is required to decode this encrypted session string")
            if not AESGCM:
                raise SessionError("cryptography library not installed or AESGCM not supported")

            if isinstance(encryption_key, str):
                key = hashlib.sha256(encryption_key.encode("utf-8")).digest()
            else:
                key = hashlib.sha256(encryption_key).digest()

            if len(raw_bytes) < 12:
                raise SessionError("Encrypted session block too short")

            nonce = raw_bytes[:12]
            ciphertext = raw_bytes[12:]
            try:
                aesgcm = AESGCM(key)
                full_block = aesgcm.decrypt(nonce, ciphertext, b"drygram_session")
            except Exception as e:
                raise SessionError(f"Failed to decrypt session string: {str(e)}")
        else:
            full_block = raw_bytes

        if len(full_block) < 8:
            raise SessionError("Session block is corrupted")

        checksum_recv = full_block[:8]
        payload = full_block[8:]

        # Verify integrity
        checksum_calc = hashlib.sha256(payload).digest()[:8]
        if checksum_recv != checksum_calc:
            raise SessionError("Session string integrity validation failed (checksum mismatch)")

        fields, _ = cls._deserialize_payload(payload)

        # Re-construct Session
        sess = cls(fields["session_id"])
        for k, v in fields.items():
            setattr(sess, k, v)
        return sess

    # ==============================================================================
    # Asynchronous Session Lifecycle Methods
    # ==============================================================================

    async def open_session(self) -> None:
        """Asynchronously load session data and open connection context."""
        await self.load()
        self.last_connected = int(time.time())
        await self.save()

    async def close_session(self) -> None:
        """Asynchronously save session data and close context."""
        self.updated_at = int(time.time())
        await self.save()

    async def destroy_session(self) -> None:
        """Permanently delete session database/storage content and clear local state."""
        await self.delete()
        self.auth_key = None
        self.auth_key_id = None
        self.server_salt = 0
        self.user_id = None
        self.bot_id = None
        self.phone_number = None
        self.username = None
        self.auth_state = "destroyed"

    async def duplicate_session(self, target_id: str) -> "Session":
        """
        Create a copy of this session with a different session ID.

        Parameters
        ----------
        target_id : str
            New session ID.

        Returns
        -------
        Session
            Duplicate session instance.
        """
        new_sess = self.__class__(target_id)
        payload = self._serialize_payload()
        fields, _ = self._deserialize_payload(payload)
        for k, v in fields.items():
            if k != "session_id":
                setattr(new_sess, k, v)
        await new_sess.save()
        return new_sess

    async def clone_session(self) -> "Session":
        """
        Create an exact duplicate of this session.

        Returns
        -------
        Session
            Cloned session.
        """
        return await self.duplicate_session(self.session_id + "_clone")

    async def rotate_session(self) -> None:
        """Rotate auth key parameters or refresh timestamps."""
        self.updated_at = int(time.time())
        await self.save()

    async def refresh_session(self) -> None:
        """Sync session timestamps and trigger save."""
        self.updated_at = int(time.time())
        await self.save()

    async def validate_session(self) -> bool:
        """Run validation checks and save state."""
        res = self.validate()
        if res:
            await self.save()
        return res

    async def repair_session(self) -> None:
        """Attempt to restore missing defaults or repair fields."""
        if not self.dc_id:
            self.dc_id = 1
        if not self.server_address:
            self.server_address = "149.154.167.50"
        if not self.server_port:
            self.server_port = 443
        await self.save()

    async def migrate_session(self, new_dc_id: int, new_address: str, new_port: int) -> None:
        """
        Migrate this session to a new DC.

        Parameters
        ----------
        new_dc_id : int
            Target DC ID.
        new_address : str
            Target DC address.
        new_port : int
            Target DC port.
        """
        self.dc_id = new_dc_id
        self.server_address = new_address
        self.server_port = new_port
        self.updated_at = int(time.time())
        await self.save()

    async def backup_session(self, target_file: str) -> None:
        """Export session string directly to a file."""
        s = self.to_string()
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(s)

    async def restore_session(self, source_file: str) -> None:
        """Restore session parameters from a session string file."""
        if not os.path.exists(source_file):
            raise SessionError("Backup file does not exist")
        with open(source_file, "r", encoding="utf-8") as f:
            s = f.read().strip()
        cloned = self.from_string(s)
        payload = cloned._serialize_payload()
        fields, _ = self._deserialize_payload(payload)
        for k, v in fields.items():
            setattr(self, k, v)
        await self.save()

    # ==============================================================================
    # Asynchronous Authorization Methods
    # ==============================================================================

    async def authorize(self) -> None:
        """Set authorization state to active."""
        self.auth_state = "authorized"
        self.updated_at = int(time.time())
        await self.save()

    async def deauthorize(self) -> None:
        """Clear authorization credentials and mark as unauthorized."""
        self.auth_state = "unauthorized"
        self.auth_key = None
        self.auth_key_id = None
        self.user_id = None
        self.bot_id = None
        self.updated_at = int(time.time())
        await self.save()

    async def logout(self) -> None:
        """Log out the current session."""
        await self.deauthorize()

    async def terminate(self) -> None:
        """Terminate the session."""
        await self.destroy_session()

    async def reconnect(self) -> None:
        """Reconnect sequence trigger."""
        self.last_connected = int(time.time())
        await self.save()

    async def reconnect_to_dc(self, dc_id: int) -> None:
        """Reconnect to a specific DC."""
        self.dc_id = dc_id
        self.last_connected = int(time.time())
        await self.save()

    async def export_authorization(self) -> bytes:
        """Export raw authorization key bytes."""
        if not self.auth_key:
            raise AuthError("Session is not authorized")
        return self.auth_key

    async def import_authorization(self, key_bytes: bytes) -> None:
        """Import authorization key bytes."""
        if len(key_bytes) != 256:
            raise AuthError("Auth key must be 256 bytes")
        self.auth_key = key_bytes
        self.auth_key_id = int.from_bytes(hashlib.sha256(key_bytes).digest()[:8], "big")
        self.auth_state = "authorized"
        await self.save()
