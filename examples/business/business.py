# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("business_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.business())
async def handle_business_client(msg: Message):
    await app.set_business_greeting("Welcome to our automated assistant!")
    await app.set_business_away("Sorry, we are currently away.")
    await app.set_business_links("https://t.me/b/chatlink")
    await app.echo(msg, "Business features successfully configured!")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
