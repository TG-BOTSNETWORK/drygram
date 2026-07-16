# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

"""
SQLite Session Storage Backend.
"""

import json
import aiosqlite
from typing import Optional
from drygram.sessions.session import Session


class SQLiteSession(Session):
    """
    SQLite based single-file local session storage engine.
    """

    def __init__(self, session_id: str, db_path: str = "drygram.session"):
        super().__init__(session_id)
        self.db_path = db_path

    async def _migrate_table(self, db: aiosqlite.Connection) -> None:
        """Ensure all required columns exist in the sessions table."""
        # Define all expected columns with their SQLite type
        columns = [
            ("api_id", "INTEGER"),
            ("test_mode", "INTEGER"),
            ("ipv6", "INTEGER"),
            ("layer", "INTEGER"),
            ("created_at", "INTEGER"),
            ("updated_at", "INTEGER"),
            ("last_connected", "INTEGER"),
            ("takeout_id", "INTEGER"),
            ("bot_id", "INTEGER"),
            ("auth_key_id", "INTEGER"),
            ("server_salt", "INTEGER"),
            ("device_model", "TEXT"),
            ("system_version", "TEXT"),
            ("app_version", "TEXT"),
            ("lang_code", "TEXT"),
            ("system_lang_code", "TEXT"),
            ("phone_number", "TEXT"),
            ("username", "TEXT"),
            ("connection_mode", "TEXT"),
            ("transport_type", "TEXT"),
            ("auth_state", "TEXT"),
            ("proxy", "TEXT")
        ]
        for col_name, col_type in columns:
            try:
                await db.execute(f"ALTER TABLE sessions ADD COLUMN {col_name} {col_type}")
                await db.commit()
            except aiosqlite.OperationalError:
                # Column already exists or table doesn't exist yet
                pass

    async def load(self) -> None:
        """Load session properties from SQLite table."""
        async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "session_id TEXT PRIMARY KEY, dc_id INTEGER, server_address TEXT, "
                "server_port INTEGER, auth_key BLOB, user_id INTEGER, is_bot INTEGER)"
            )
            await db.commit()
            await self._migrate_table(db)

            query = (
                "SELECT dc_id, server_address, server_port, auth_key, user_id, is_bot, "
                "api_id, test_mode, ipv6, layer, created_at, updated_at, last_connected, "
                "takeout_id, bot_id, auth_key_id, server_salt, device_model, system_version, "
                "app_version, lang_code, system_lang_code, phone_number, username, "
                "connection_mode, transport_type, auth_state, proxy "
                "FROM sessions WHERE session_id = ?"
            )
            async with db.execute(query, (self.session_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    self.dc_id = row[0] or 1
                    self.server_address = row[1] or "149.154.167.50"
                    self.server_port = row[2] or 443
                    self.auth_key = row[3]
                    self.user_id = row[4]
                    self.is_bot = bool(row[5])
                    self.api_id = row[6] or 0
                    self.test_mode = bool(row[7])
                    self.ipv6 = bool(row[8])
                    self.layer = row[9] or 184
                    self.created_at = row[10] or self.created_at
                    self.updated_at = row[11] or self.updated_at
                    self.last_connected = row[12] or 0
                    self.takeout_id = row[13]
                    self.bot_id = row[14]
                    self.auth_key_id = row[15]
                    self.server_salt = row[16] or 0
                    self.device_model = row[17] or "Unknown Device"
                    self.system_version = row[18] or "Unknown System"
                    self.app_version = row[19] or "1.0.0"
                    self.lang_code = row[20] or "en"
                    self.system_lang_code = row[21] or "en"
                    self.phone_number = row[22]
                    self.username = row[23]
                    self.connection_mode = row[24] or "tcp"
                    self.transport_type = row[25] or "intermediate"
                    self.auth_state = row[26] or "unauthorized"
                    
                    proxy_str = row[27]
                    if proxy_str:
                        try:
                            self.proxy = json.loads(proxy_str)
                        except Exception:
                            self.proxy = None

    async def save(self) -> None:
        """Save session properties to SQLite table."""
        async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "session_id TEXT PRIMARY KEY, dc_id INTEGER, server_address TEXT, "
                "server_port INTEGER, auth_key BLOB, user_id INTEGER, is_bot INTEGER)"
            )
            await db.commit()
            await self._migrate_table(db)

            query = (
                "INSERT OR REPLACE INTO sessions ("
                "session_id, dc_id, server_address, server_port, auth_key, user_id, is_bot, "
                "api_id, test_mode, ipv6, layer, created_at, updated_at, last_connected, "
                "takeout_id, bot_id, auth_key_id, server_salt, device_model, system_version, "
                "app_version, lang_code, system_lang_code, phone_number, username, "
                "connection_mode, transport_type, auth_state, proxy"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )
            proxy_str = json.dumps(self.proxy) if self.proxy else None
            await db.execute(
                query,
                (
                    self.session_id,
                    self.dc_id,
                    self.server_address,
                    self.server_port,
                    self.auth_key,
                    self.user_id,
                    1 if self.is_bot else 0,
                    self.api_id,
                    1 if self.test_mode else 0,
                    1 if self.ipv6 else 0,
                    self.layer,
                    self.created_at,
                    self.updated_at,
                    self.last_connected,
                    self.takeout_id,
                    self.bot_id,
                    self.auth_key_id,
                    self.server_salt,
                    self.device_model,
                    self.system_version,
                    self.app_version,
                    self.lang_code,
                    self.system_lang_code,
                    self.phone_number,
                    self.username,
                    self.connection_mode,
                    self.transport_type,
                    self.auth_state,
                    proxy_str
                )
            )
            await db.commit()

    async def delete(self) -> None:
        """Erase the current session record from SQLite database."""
        async with aiosqlite.connect(self.db_path, timeout=30.0) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "session_id TEXT PRIMARY KEY, dc_id INTEGER, server_address TEXT, "
                "server_port INTEGER, auth_key BLOB, user_id INTEGER, is_bot INTEGER)"
            )
            await db.commit()
            await db.execute("DELETE FROM sessions WHERE session_id = ?", (self.session_id,))
            await db.commit()
        self.auth_key = None
        self.auth_key_id = None
        self.user_id = None
        self.bot_id = None
        self.auth_state = "destroyed"
