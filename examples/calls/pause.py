# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

async def main():
    client = DryClient("session_name", api_id=12345, api_hash="abc")
    call_client = PyTgCalls(client)

    await client.start()
    await call_client.start()

    await call_client.join_group_call(
        chat_id=-10012345678,
        stream=AudioPiped("examples/media/sample.mp3")
    )

    await asyncio.sleep(5)
    print("Pausing stream...")
    await call_client.pause_stream(chat_id=-10012345678)

if __name__ == "__main__":
    asyncio.run(main())
