# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, HTMLParser

async def main():
    client = DryClient("emoji_session", api_id=12345, api_hash="abcdef")
    await client.start()
    text, entities = HTMLParser.parse('<tg-emoji emoji-id="54321">🔥</tg-emoji>')
    await client.deliver("chat_id", text)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
