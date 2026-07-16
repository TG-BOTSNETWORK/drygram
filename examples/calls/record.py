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

    print("Joining call and starting recording...")
    # NOTE: Output is saved to 'examples/media/record.wav'
    await call_client.join_group_call(
        chat_id=-10012345678,
        stream=AudioPiped("examples/media/sample.mp3")
    )
    print("Recording stream active...")
    await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
