# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("download_session", api_id=12345, api_hash="abcdef")
    await client.start()
    file_bytes = await client.collect("doc_12345")
    print(f"Downloaded file bytes: {len(file_bytes)}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
