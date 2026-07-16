# PostgreSQL Storage

The PostgreSQL session backend uses `asyncpg` to save authorization keys and states asynchronously to a relational Postgres database.

## Configuration

```python
from drygram import DryClient
from drygram.sessions.postgres import PostgresSession

session = PostgresSession(
    host="localhost",
    port=5432,
    user="postgres",
    password="my_password",
    database="drygram",
    session_id="user_123"
)
client = DryClient(session, api_id=123, api_hash="abc")
```
