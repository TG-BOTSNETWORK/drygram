# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.errors.rpc import FloodWait

async def main():
    client = DryClient("flood_session", api_id=12345, api_hash="abcdef")
    await client.start()
    try:
        raise FloodWait(10)
    except FloodWait as e:
        print(f"Rate limited. Waiting for {e.retry_time} seconds.")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
