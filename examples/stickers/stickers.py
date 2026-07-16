# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("stickers_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("sticker"))
async def send_sticker_example(msg: Message):
    await app.deliver_file(
        chat_id=msg.chat.id,
        file="path/to/sticker.webp",
        caption="Premium Sticker"
    )

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
