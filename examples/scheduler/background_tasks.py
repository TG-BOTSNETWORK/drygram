# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def background_worker():
    while True:
        print("Running background task...")
        await asyncio.sleep(5)

async def main():
    client = DryClient("bg_session", api_id=12345, api_hash="abcdef")
    await client.start()
    asyncio.create_task(background_worker())
    await asyncio.sleep(15)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
