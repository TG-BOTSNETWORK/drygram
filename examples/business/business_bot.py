# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("business_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.business())
async def auto_reply(msg: Message):
    await app.echo(msg, "Thank you for reaching out to our business!")

async def main():
    await app.start()
    await app.set_business_greeting("Hello! How can we help you today?")
    await app.set_business_away("We are currently out of office.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
