# Quick Start

Get up and running with a simple echo bot.

```python
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("my_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.private() & Gates.text("ping"))
async def ping_handler(msg: Message):
    await app.echo(msg, "pong")

async def main():
    await app.start()
    print("Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```
