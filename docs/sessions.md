# Session Engines

DryGram supports multiple session engines for scalability.

- **SQLite**: Local single-file storage.
- **PostgreSQL**: Production clustered storage.
- **Redis**: Fast cache storage.
- **MongoDB**: Document storage.
- **Memory**: Ephemeral storage.

```python
from drygram import DryClient, RedisSession
session = RedisSession("session_id", redis_url="redis://localhost:6379/0")
client = DryClient(session, api_id=123, api_hash="abc")
```
