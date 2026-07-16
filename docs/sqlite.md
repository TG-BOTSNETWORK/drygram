# SQLite Storage

The default storage backend. It uses `aiosqlite` to write credentials and active connection metadata to a local SQLite database file.

## Configuration

Pass a path string directly to the client constructor:

```python
from drygram import DryClient

# Automatically initializes a local SQLite file named my_session.session
client = DryClient("my_session", api_id=123, api_hash="abc")
```
