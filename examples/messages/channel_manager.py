# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("channel_manager_session", api_id=12345, api_hash="abcdef")
    await client.start()
    await client.deliver("@my_channel", "Important channel announcement!")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
