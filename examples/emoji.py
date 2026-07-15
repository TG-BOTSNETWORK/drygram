# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message, HTMLParser

app = DryClient("emoji_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("emoji"))
async def custom_emoji_example(msg: Message):
    text, entities = HTMLParser.parse('<tg-emoji emoji-id="54321">🔥</tg-emoji>')
    await app.deliver(
        chat_id=msg.chat.id,
        text=text,
        effect_id="effect_sparkle"
    )

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
