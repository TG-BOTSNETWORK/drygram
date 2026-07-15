# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("inline_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("inline_query"))
async def handle_inline_query(msg: Message):
    await app.echo(msg, "Sending inline query results")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
