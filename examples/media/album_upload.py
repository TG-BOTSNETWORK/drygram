# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, MediaGroup, Photo, Video

async def main():
    client = DryClient("album_session", api_id=12345, api_hash="abcdef")
    await client.start()
    photo = Photo(file_id="photo_id", file_unique_id="p1", width=10, height=10, file_size=100)
    video = Video(file_id="video_id", file_unique_id="v1", width=10, height=10, duration=5, file_size=200)
    album = MediaGroup(id="album_123", media_list=[photo, video])
    await client.deliver("chat_id", "Media album:", markup=album)
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
