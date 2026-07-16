# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("export_session", api_id=12345, api_hash="abcdef")
    await client.start()
    auth_key = client.session.auth_key
    print(f"Exported Auth Key: {auth_key.hex() if auth_key else None}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
