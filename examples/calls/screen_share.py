# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioVideoPiped

async def main():
    client = DryClient("session_name", api_id=12345, api_hash="abc")
    call_client = PyTgCalls(client)

    await client.start()
    await call_client.start()

    print("Screen sharing using video pipeline...")
    # NOTE: Replace with screen device input or screen share video file 'examples/media/sample.mov'
    await call_client.join_group_call(
        chat_id=-10012345678,
        stream=AudioVideoPiped("examples/media/sample.mov")
    )

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
