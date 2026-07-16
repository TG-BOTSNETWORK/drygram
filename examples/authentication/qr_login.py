# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("qr_session", api_id=12345, api_hash="abcdef")
    await client.start()
    qr_link = await client.request_qr_code()
    print(f"Login link: {qr_link}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
