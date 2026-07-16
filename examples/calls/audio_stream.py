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

    print("Streaming audio file...")
    # NOTE: Replace 'examples/media/sample.wav' with a real wav file path
    await call_client.join_group_call(
        chat_id=-10012345678,
        stream=AudioPiped("examples/media/sample.wav")
    )

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
