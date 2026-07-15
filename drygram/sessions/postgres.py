# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncpg
from typing import Optional
from drygram.sessions.base import BaseSession

class PostgresSession(BaseSession):
    """
    PostgreSQL based SQL session storage engine.

    Parameters
    ----------
    session_id : str
        Unique identifier for the session.
    dsn : str
        PostgreSQL connection DSN.

    Attributes
    ----------
    dsn : str
        Connection string parameter.
    """

    def __init__(self, session_id: str, dsn: str):
        """
        Initialize the PostgresSession.

        Parameters
        ----------
        session_id : str
            Unique session ID.
        dsn : str
            Postgres DSN URI.
        """
        super().__init__(session_id)
        self.dsn = dsn

    async def load(self) -> None:
        """Load session properties from PostgreSQL database table."""
        conn = await asyncpg.connect(self.dsn)
        try:
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS drygram_sessions ("
                "session_id VARCHAR(255) PRIMARY KEY, dc_id INTEGER, server_address VARCHAR(255), "
                "server_port INTEGER, auth_key BYTEA, user_id BIGINT, is_bot BOOLEAN)"
            )
            row = await conn.fetchrow(
                "SELECT dc_id, server_address, server_port, auth_key, user_id, is_bot "
                "FROM drygram_sessions WHERE session_id = $1",
                self.session_id
            )
            if row:
                self.dc_id = row["dc_id"]
                self.server_address = row["server_address"]
                self.server_port = row["server_port"]
                self.auth_key = row["auth_key"]
                self.user_id = row["user_id"]
                self.is_bot = row["is_bot"]
        finally:
            await conn.close()

    async def save(self) -> None:
        """Save session properties to PostgreSQL database table."""
        conn = await asyncpg.connect(self.dsn)
        try:
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS drygram_sessions ("
                "session_id VARCHAR(255) PRIMARY KEY, dc_id INTEGER, server_address VARCHAR(255), "
                "server_port INTEGER, auth_key BYTEA, user_id BIGINT, is_bot BOOLEAN)"
            )
            await conn.execute(
                "INSERT INTO drygram_sessions "
                "(session_id, dc_id, server_address, server_port, auth_key, user_id, is_bot) "
                "VALUES ($1, $2, $3, $4, $5, $6, $7) "
                "ON CONFLICT (session_id) DO UPDATE SET "
                "dc_id = EXCLUDED.dc_id, server_address = EXCLUDED.server_address, "
                "server_port = EXCLUDED.server_port, auth_key = EXCLUDED.auth_key, "
                "user_id = EXCLUDED.user_id, is_bot = EXCLUDED.is_bot",
                self.session_id,
                self.dc_id,
                self.server_address,
                self.server_port,
                self.auth_key,
                self.user_id,
                self.is_bot
            )
        finally:
            await conn.close()

    async def delete(self) -> None:
        """Erase the current session record from PostgreSQL database."""
        conn = await asyncpg.connect(self.dsn)
        try:
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS drygram_sessions ("
                "session_id VARCHAR(255) PRIMARY KEY, dc_id INTEGER, server_address VARCHAR(255), "
                "server_port INTEGER, auth_key BYTEA, user_id BIGINT, is_bot BOOLEAN)"
            )
            await conn.execute("DELETE FROM drygram_sessions WHERE session_id = $1", self.session_id)
        finally:
            await conn.close()
        self.auth_key = None
        self.user_id = None
        self.is_bot = False
