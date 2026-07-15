# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import aiosqlite
from drygram.sessions.base import BaseSession

class SQLiteSession(BaseSession):
    """
    SQLite based single-file local session storage engine.

    Parameters
    ----------
    session_id : str
        Unique identifier for the session.
    db_path : str, default="drygram.session"
        Path to the SQLite database file.

    Attributes
    ----------
    db_path : str
        Database path reference.
    """

    def __init__(self, session_id: str, db_path: str = "drygram.session"):
        """
        Initialize the SQLiteSession.

        Parameters
        ----------
        session_id : str
            Unique session ID.
        db_path : str, default="drygram.session"
            Local SQLite DB file path.
        """
        super().__init__(session_id)
        self.db_path = db_path

    async def load(self) -> None:
        """Load session properties from SQLite table."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "session_id TEXT PRIMARY KEY, dc_id INTEGER, server_address TEXT, "
                "server_port INTEGER, auth_key BLOB, user_id INTEGER, is_bot INTEGER)"
            )
            await db.commit()
            async with db.execute(
                "SELECT dc_id, server_address, server_port, auth_key, user_id, is_bot "
                "FROM sessions WHERE session_id = ?",
                (self.session_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    self.dc_id = row[0]
                    self.server_address = row[1]
                    self.server_port = row[2]
                    self.auth_key = row[3]
                    self.user_id = row[4]
                    self.is_bot = bool(row[5])

    async def save(self) -> None:
        """Save session properties to SQLite table."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "session_id TEXT PRIMARY KEY, dc_id INTEGER, server_address TEXT, "
                "server_port INTEGER, auth_key BLOB, user_id INTEGER, is_bot INTEGER)"
            )
            await db.commit()
            await db.execute(
                "INSERT OR REPLACE INTO sessions "
                "(session_id, dc_id, server_address, server_port, auth_key, user_id, is_bot) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    self.session_id,
                    self.dc_id,
                    self.server_address,
                    self.server_port,
                    self.auth_key,
                    self.user_id,
                    1 if self.is_bot else 0
                )
            )
            await db.commit()

    async def delete(self) -> None:
        """Erase the current session record from SQLite database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "session_id TEXT PRIMARY KEY, dc_id INTEGER, server_address TEXT, "
                "server_port INTEGER, auth_key BLOB, user_id INTEGER, is_bot INTEGER)"
            )
            await db.commit()
            await db.execute("DELETE FROM sessions WHERE session_id = ?", (self.session_id,))
            await db.commit()
        self.auth_key = None
        self.user_id = None
        self.is_bot = False
