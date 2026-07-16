# High-Level Client API

The `DryClient` class is the central entrypoint to DryGram, managing active connections, update dispatching, and executing schema RPC requests.

## Initialization

Configure client instances with api credentials, bot token, or custom proxies:

```python
from drygram import DryClient

client = DryClient("my_session", api_id=123, api_hash="abc")
```

## Running the Client

Initialize connection loops:

```python
# Synchronous setup using asyncio.run
import asyncio

async def main():
    await client.start()
    print("Engine active.")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```
