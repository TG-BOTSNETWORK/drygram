# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("echo_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.private() & Gates.text("ping"))
async def ping_responder(msg: Message):
    await app.echo(msg, "pong")

@app.observe(Gates.private() & ~Gates.text("ping"))
async def echo_responder(msg: Message):
    if msg.text:
        await app.echo(msg, msg.text)

async def main():
    await app.start()
    await asyncio.sleep(5)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
