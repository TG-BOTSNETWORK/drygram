# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("retry_session", api_id=12345, api_hash="abcdef")
    await client.start()
    # DryClient automatically retries failed connection queries internally
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
