# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("uploads_session", api_id=12345, api_hash="abcdef")

def progress(current, total):
    print(f"Uploaded: {current}/{total} bytes ({(current/total)*100:.1f}%)")

@app.observe(Gates.text("upload"))
async def handle_upload(msg: Message):
    await app.deliver_file(
        chat_id=msg.chat.id,
        file=b"large_file_binary_payload",
        caption="Chunk Upload Demonstration",
        progress_callback=progress
    )

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
