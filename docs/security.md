# Security Practices

This guide describes the cryptographic and storage design choices that protect credentials in DryGram.

## Session Encryption

Use `EncryptedSession` to encrypt authorization key blocks with AES-256-GCM before writing to the local disk:

```python
from drygram.sessions.encrypted import EncryptedSession

# Enforce secure database storage
session = EncryptedSession("my_db.session", password="my_password")
```

## Transport Security

All packets written to Telegram data centers are encrypted using AES-IGE crypt ciphers as defined by MTProto specifications.
