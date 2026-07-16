# MongoDB Storage

The MongoDB storage backend uses `motor` for asynchronous connections to document databases.

## Configuration

```python
from drygram import DryClient
from drygram.sessions.mongo import MongoSession

session = MongoSession(
    host="localhost",
    port=27017,
    database="drygram_db",
    collection="sessions",
    session_id="user_123"
)
client = DryClient(session, api_id=123, api_hash="abc")
```
