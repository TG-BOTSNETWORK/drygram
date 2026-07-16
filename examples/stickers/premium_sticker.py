# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("premium_sticker_session", api_id=12345, api_hash="abcdef")
    await client.start()
    await client.deliver_file("chat_id", "premium_sticker.webp")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
