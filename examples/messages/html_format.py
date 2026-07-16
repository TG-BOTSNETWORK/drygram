# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, HTMLParser

async def main():
    client = DryClient("html_session", api_id=12345, api_hash="abcdef")
    await client.start()
    text, entities = HTMLParser.parse("This is <b>bold</b> and <i>italic</i> HTML text.")
    await client.deliver("chat_id", text)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
