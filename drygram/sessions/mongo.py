# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import motor.motor_asyncio
from typing import Optional
from drygram.sessions.base import BaseSession

class MongoSession(BaseSession):
    """
    MongoDB based NoSQL remote session storage engine.

    Parameters
    ----------
    session_id : str
        Unique identifier for the session.
    connection_string : str
        MongoDB connection URI.
    db_name : str, default="drygram_db"
        Name of the database.

    Attributes
    ----------
    connection_string : str
        Target URI.
    db_name : str
        Database name.
    """

    def __init__(self, session_id: str, connection_string: str, db_name: str = "drygram_db"):
        """
        Initialize the MongoSession.

        Parameters
        ----------
        session_id : str
            Unique session ID.
        connection_string : str
            Mongo connection URI.
        db_name : str, default="drygram_db"
            Target database.
        """
        super().__init__(session_id)
        self.connection_string = connection_string
        self.db_name = db_name

    async def load(self) -> None:
        """Load session properties from MongoDB collection document."""
        client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
        db = client[self.db_name]
        collection = db["sessions"]
        doc = await collection.find_one({"session_id": self.session_id})
        if doc:
            self.dc_id = doc.get("dc_id", 1)
            self.server_address = doc.get("server_address", "149.154.167.50")
            self.server_port = doc.get("server_port", 443)
            self.auth_key = doc.get("auth_key")
            self.user_id = doc.get("user_id")
            self.is_bot = doc.get("is_bot", False)
        client.close()

    async def save(self) -> None:
        """Save session properties to MongoDB collection document."""
        client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
        db = client[self.db_name]
        collection = db["sessions"]
        await collection.replace_one(
            {"session_id": self.session_id},
            {
                "session_id": self.session_id,
                "dc_id": self.dc_id,
                "server_address": self.server_address,
                "server_port": self.server_port,
                "auth_key": self.auth_key,
                "user_id": self.user_id,
                "is_bot": self.is_bot
            },
            upsert=True
        )
        client.close()

    async def delete(self) -> None:
        """Erase the current session record from MongoDB."""
        client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
        db = client[self.db_name]
        collection = db["sessions"]
        await collection.delete_one({"session_id": self.session_id})
        client.close()
        self.auth_key = None
        self.user_id = None
        self.is_bot = False
