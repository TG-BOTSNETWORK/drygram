# Redis Storage

The Redis session storage backend uses `redis-py` to cache session attributes in memory, providing fast read/write performance.

## Configuration

```python
from drygram import DryClient
from drygram.sessions.redis import RedisSession

session = RedisSession(
    host="localhost",
    port=6379,
    db=0,
    session_id="user_123"
)
client = DryClient(session, api_id=123, api_hash="abc")
```
