# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("api_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.private())
async def handle_message(msg: Message):
    print(f"Incoming: {msg.text}")

async def main():
    await app.start()
    await app.deliver("chat_id", "Testing full original API suite.")
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
