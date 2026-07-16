# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("admin_tools_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.group() & Gates.text("/pin"))
async def pin_message(msg: Message):
    if msg.reply_to_message:
        await app.anchor(msg.chat.id, msg.reply_to_message.id)
        await app.echo(msg, "Message pinned.")

async def main():
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
