# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message, PremiumEmojiStatus

app = DryClient("premium_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.premium())
async def premium_handler(msg: Message):
    status = PremiumEmojiStatus(emoji_id="emoji_123", document_id="doc_456")
    await app.echo(msg, f"Premium user status: {status.emoji_id}")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
