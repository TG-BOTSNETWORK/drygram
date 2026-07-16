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

    playlist = [
        "examples/media/sample.mp3",
        "examples/media/sample.wav",
        "examples/media/sample.ogg"
    ]

    for song in playlist:
        print(f"Playing next song: {song}")
        await call_client.join_group_call(
            chat_id=-10012345678,
            stream=AudioPiped(song)
        )
        # Play each song for 10 seconds in this demonstration
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
