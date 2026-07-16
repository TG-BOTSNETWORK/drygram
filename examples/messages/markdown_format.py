# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, MarkdownParser

async def main():
    client = DryClient("md_session", api_id=12345, api_hash="abcdef")
    await client.start()
    text, entities = MarkdownParser.parse("This is **bold** and *italic* text.")
    await client.deliver("chat_id", text)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
 Maroon formatting Example
