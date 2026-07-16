# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("downloads_session", api_id=12345, api_hash="abcdef")

def progress(current, total):
    print(f"Downloaded: {current}/{total} bytes ({(current/total)*100:.1f}%)")

@app.observe(Gates.text("download"))
async def handle_download(msg: Message):
    data = await app.collect("file_id_to_retrieve", progress_callback=progress)
    print(f"File downloaded successfully. Size: {len(data)} bytes.")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
