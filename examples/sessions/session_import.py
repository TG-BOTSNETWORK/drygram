# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, MemorySession

async def main():
    sess = MemorySession("imported")
    sess.auth_key = b"dummy_imported_auth_key_data"
    client = DryClient(sess, api_id=12345, api_hash="abcdef")
    await client.start()
    print(f"Client started using imported session key: {client.session.auth_key}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
