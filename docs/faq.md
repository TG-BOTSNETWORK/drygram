# Frequently Asked Questions (FAQ)

### 1. Does DryGram support Pyrogram session strings?
No. DryGram uses a completely custom, versioned, URL-safe base64 session serialization format (`DRY1` format) featuring SHA256 payload integrity checksums and optional AES-256-GCM encryption.

### 2. Can I use DryGram to run both bot and user accounts?
Yes. DryGram supports bot token authentication (`bot_login()`) and interactive user authorizations.

### 3. How do I change the default SQLite database path?
When instantiating `DryClient`, pass a filename string (which defaults to a local SQLite session) or construct a session backend:

```python
from drygram import DryClient
from drygram.sessions.sqlite import SQLiteSession

# Save to a custom path
session = SQLiteSession("my_data/custom_path.session")
client = DryClient(session, api_id=123, api_hash="abc")
```

### 4. How can I handle FloodWait exceptions?
DryGram raises a `FloodWait` exception containing a `retry_time` attribute. Handle it in your code using standard try/except blocks:

```python
from drygram.errors.rpc import FloodWait

try:
    await client.deliver(123456, "Hello!")
except FloodWait as e:
    print(f"Rate limit exceeded. Waiting for {e.retry_time}s")
    await asyncio.sleep(e.retry_time)
```
