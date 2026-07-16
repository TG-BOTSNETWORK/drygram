# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

async def main():
    client = DryClient("session_name", api_id=12345, api_hash="abc")
    call_client = PyTgCalls(client)

    # Start DryGram and PyTgCalls
    await client.start()
    await call_client.start()

    print("Joining voice chat...")
    # NOTE: Replace 'examples/media/sample.mp3' with a real audio file path
    await call_client.join_group_call(
        chat_id=-10012345678,
        stream=AudioPiped("examples/media/sample.mp3")
    )

    print("Running voice chat. Press Ctrl+C to exit.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
