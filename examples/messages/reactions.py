# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("reactions_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("react"))
async def handle_react(msg: Message):
    await app.echo(msg, "Reacting with thumb up!")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
