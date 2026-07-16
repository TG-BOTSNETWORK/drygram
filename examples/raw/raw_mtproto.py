# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("raw_session", api_id=12345, api_hash="abcdef")
    await client.start()
    raw_response = await client.primitive("my_chat_name")
    print(f"Raw channel data: {raw_response}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
