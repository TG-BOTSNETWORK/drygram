# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient

async def main():
    client = DryClient("hello_session", api_id=12345, api_hash="abcdef")
    await client.start()
    print(f"Logged in as: {client.me.first_name}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
