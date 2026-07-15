# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message, MediaGroup, Photo, Video

app = DryClient("album_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("album"))
async def send_album(msg: Message):
    photo = Photo(file_id="photo1", file_unique_id="p1", width=100, height=100, file_size=50)
    video = Video(file_id="video1", file_unique_id="v1", width=200, height=200, duration=10, file_size=200)
    album = MediaGroup(id="album_123", media_list=[photo, video])
    await app.deliver(chat_id=msg.chat.id, text="Here is the media album:", markup=album)

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
