# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    proxy = {"type": "socks5", "addr": "127.0.0.1", "port": 1080}
    client = DryClient("proxy_session", api_id=12345, api_hash="abcdef", proxy=proxy)
    await client.start()
    print("Connected via SOCKS5 proxy successfully.")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
