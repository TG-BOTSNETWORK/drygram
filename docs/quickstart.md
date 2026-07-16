# Quick Start Guide

This guide helps you build and launch your first DryGram application.

## Client Initialization

To get started, obtain an `api_id` and `api_hash` from the official [Telegram Apps page](https://my.telegram.org/).

### Bot Authorization
To log in as a bot using a token generated from @BotFather:

```python
import asyncio
from drygram import DryClient

async def main():
    app = DryClient("bot_session", api_id=12345, api_hash="abcdef")
    await app.start()
    
    # Log in using the bot token
    bot_user = await app.bot_login("123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
    print(f"Logged in as bot: {bot_user.username}")
    
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### User Authorization (Interactive)
To authorize a user account, DryGram handles interactive console login out of the box:

```python
import asyncio
from drygram import DryClient

async def main():
    app = DryClient("user_session", api_id=12345, api_hash="abcdef")
    
    # Starting the client interactive login
    await app.start()
    
    # If not authorized, ask for phone, verification code, and 2FA password
    if not app.me:
        phone = input("Enter phone number (international): ")
        hash_val = await app.request_login_code(phone)
        code = input("Enter code: ")
        try:
            user = await app.complete_login(phone, hash_val, code)
        except Exception:
            # 2FA password handling
            password = input("Enter 2FA password: ")
            await app.submit_password(password)
            
    print(f"Logged in as user: {app.me.first_name}")
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Echo Event Handler

Let's write a simple bot that responds with "pong" when it receives a private text message saying "ping", and echoes back other private text messages:

```python
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("echo_session", api_id=12345, api_hash="abcdef")

# Observers receive matching updates from the dispatcher
@app.observe(Gates.private() & Gates.text("ping"))
async def ping_responder(msg: Message):
    await app.echo(msg, "pong")

@app.observe(Gates.private() & ~Gates.text("ping"))
async def echo_responder(msg: Message):
    if msg.text:
        await app.echo(msg, msg.text)

async def main():
    await app.start()
    # Run the client loop until interrupted
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
```
