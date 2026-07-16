# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("media_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("/sendmedia"))
async def send_media(msg: Message):
    await app.deliver_image(msg.chat.id, "path/to/photo.jpg", "Here is a photo")
    await app.deliver_video(msg.chat.id, "path/to/video.mp4", "Here is a video")

async def main():
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
