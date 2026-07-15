# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message, CallParticipant

app = DryClient("video_session", api_id=12345, api_hash="abcdef")

def on_join(participant: CallParticipant):
    print(f"User joined video call: {participant.user_id}")

@app.observe(Gates.text("join_video"))
async def video_chat_example(msg: Message):
    await app.enter(msg.chat.id)
    app.calls.on_participant_event(on_join)
    await app.calls.stream_video(msg.chat.id, "camera.mp4")
    await app.calls.set_volume(100)
    await app.echo(msg, "Video chat active. Streaming video...")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
