# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("pwd_session", api_id=12345, api_hash="abcdef")
    await client.start()
    success = await client.submit_password("secure_2fa_password")
    print(f"2FA login status: {success}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
