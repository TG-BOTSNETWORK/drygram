# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("sticker_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("/sendsticker"))
async def send_sticker(msg: Message):
    await app.deliver_file(msg.chat.id, "path/to/sticker.webp")

async def main():
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
