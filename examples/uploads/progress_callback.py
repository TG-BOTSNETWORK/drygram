# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

def progress(current, total):
    print(f"Progress: {current}/{total} bytes ({(current/total)*100:.1f}%)")

async def main():
    client = DryClient("progress_session", api_id=12345, api_hash="abcdef")
    await client.start()
    await client.deliver_file("chat_id", b"large_data", progress_callback=progress)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
