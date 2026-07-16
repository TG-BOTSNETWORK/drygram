# Raw MTProto Protocol Reference

DryGram exposes a low-level Raw API module under `drygram.raw` allowing developers to compile and invoke raw MTProto schema functions directly.

## Sending Raw Requests

Use `client.engine.send_rpc` or the client's `primitive()` wrapper (if implemented) to execute raw requests:

```python
from drygram import DryClient
from drygram.raw import Ping

app = DryClient("session", api_id=123, api_hash="abc")

async def main():
    await app.start()
    
    # Send a raw MTProto Ping request
    ping_request = Ping(ping_id=88888)
    pong_response = await app.engine.send_rpc(ping_request)
    print(f"Server returned pong with ID: {pong_response.ping_id}")
    
    await app.stop()
```

## Schema Compilation

DryGram's parser dynamically parses incoming TL-structured binary blocks. It resolves constructor IDs by mapping them to classes registered in `TLRegistry`.
