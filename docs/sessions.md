# Session Management Guide

DryGram provides a robust, pluggable session persistence layer built on a unified `Session` base class. It stores DC configurations, server addresses, authorization keys, client IDs, and user/bot metadata.

## Pluggable Session Backends

DryGram supports multiple local and remote session storage backends:

| Backend | Class | Requirements | Storage Location |
|---|---|---|---|
| **SQLite (Default)** | `SQLiteSession` | `aiosqlite` | Local SQLite Database file |
| **JSON** | `JSONSession` | *None* | Plain-text JSON file |
| **Binary** | `BinarySession` | *None* | Packed binary blocks file |
| **Encrypted Binary** | `EncryptedSession` | `cryptography` | AES-256-GCM encrypted file |
| **Memory** | `MemorySession` | *None* | Ephemeral memory storage |
| **PostgreSQL** | `PostgresSession` | `asyncpg` | Remote PostgreSQL table |
| **Redis** | `RedisSession` | `redis` | Remote Redis cache server |
| **MongoDB** | `MongoSession` | `motor` | Remote MongoDB collection |
| **Custom** | `CustomSession` | *None* | Custom developer async callbacks |

### Configuring a Session Backend

Pass the session instance directly to the client constructor:

```python
from drygram import DryClient
from drygram.sessions.redis import RedisSession

# Storing session state in a Redis server
session = RedisSession(host="localhost", port=6379, db=0, session_id="my_session")
client = DryClient(session, api_id=123, api_hash="abc")
```

---

## DryGram Session String (DRY1 Format)

DryGram features an original, versioned, URL-safe base64 session string format. It allows transferring session states (including authorization keys) directly between deployments without sharing files.

There are two forms of the Session String:

1. **Unencrypted (`DRY1U_` prefix)**:
   Contains session metadata and the raw auth key, verified by a SHA256 checksum of the payload.
2. **Encrypted (`DRY1E_` prefix)**:
   Encrypts the payload using AES-256-GCM using a developer-supplied password/key.

### Exporting Session String

```python
# Export an unencrypted session string
sess_str = client.export_session()
print(sess_str)
# Output: DRY1U_gAAAAABn...

# Export an encrypted session string
secure_str = client.export_session(encryption_key="my_secure_password")
```

### Importing Session String

```python
# Initialize an empty SQLite session
new_client = DryClient("cloned_session", api_id=123, api_hash="abc")

# Import the session string
await new_client.import_session(sess_str)
```
