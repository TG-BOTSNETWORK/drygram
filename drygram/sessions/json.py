# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

"""
JSON Session Storage Backend.
"""

import os
import json
import base64
import time
from typing import Optional
from drygram.sessions.session import Session
from drygram.errors.rpc import SessionError


class JSONSession(Session):
    """
    Saves/loads session state as a JSON text file on disk.
    """

    def __init__(self, session_id: str, filepath: Optional[str] = None):
        super().__init__(session_id)
        self.filepath = filepath or f"{session_id}.json"

    async def load(self) -> None:
        """Load session fields from JSON file."""
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Map JSON values back to fields
            self.api_id = data.get("api_id", 0)
            self.dc_id = data.get("dc_id", 1)
            self.server_address = data.get("server_address", "149.154.167.50")
            self.server_port = data.get("server_port", 443)
            self.test_mode = data.get("test_mode", False)
            self.ipv6 = data.get("ipv6", False)
            self.layer = data.get("layer", 184)
            self.created_at = data.get("created_at", int(time.time() if "time" in globals() else 0))
            self.updated_at = data.get("updated_at", int(time.time() if "time" in globals() else 0))
            self.last_connected = data.get("last_connected", 0)
            self.takeout_id = data.get("takeout_id")
            self.user_id = data.get("user_id")
            self.bot_id = data.get("bot_id")
            self.is_bot = data.get("is_bot", False)
            self.auth_key_id = data.get("auth_key_id")
            self.server_salt = data.get("server_salt", 0)
            self.device_model = data.get("device_model", "Unknown Device")
            self.system_version = data.get("system_version", "Unknown System")
            self.app_version = data.get("app_version", "1.0.0")
            self.lang_code = data.get("lang_code", "en")
            self.system_lang_code = data.get("system_lang_code", "en")
            self.phone_number = data.get("phone_number")
            self.username = data.get("username")
            self.connection_mode = data.get("connection_mode", "tcp")
            self.transport_type = data.get("transport_type", "intermediate")
            self.auth_state = data.get("auth_state", "unauthorized")
            self.proxy = data.get("proxy")

            auth_key_b64 = data.get("auth_key")
            if auth_key_b64:
                self.auth_key = base64.b64decode(auth_key_b64)
            else:
                self.auth_key = None
        except Exception as e:
            raise SessionError(f"Failed to load JSON session: {str(e)}")

    async def save(self) -> None:
        """Save session fields to JSON file."""
        try:
            data = {
                "api_id": self.api_id,
                "dc_id": self.dc_id,
                "server_address": self.server_address,
                "server_port": self.server_port,
                "test_mode": self.test_mode,
                "ipv6": self.ipv6,
                "layer": self.layer,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "last_connected": self.last_connected,
                "takeout_id": self.takeout_id,
                "user_id": self.user_id,
                "bot_id": self.bot_id,
                "is_bot": self.is_bot,
                "auth_key_id": self.auth_key_id,
                "server_salt": self.server_salt,
                "device_model": self.device_model,
                "system_version": self.system_version,
                "app_version": self.app_version,
                "lang_code": self.lang_code,
                "system_lang_code": self.system_lang_code,
                "phone_number": self.phone_number,
                "username": self.username,
                "connection_mode": self.connection_mode,
                "transport_type": self.transport_type,
                "auth_state": self.auth_state,
                "proxy": self.proxy,
                "auth_key": base64.b64encode(self.auth_key).decode("utf-8") if self.auth_key else None
            }
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise SessionError(f"Failed to save JSON session: {str(e)}")

    async def delete(self) -> None:
        """Delete the JSON session file."""
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
