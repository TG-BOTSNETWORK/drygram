# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("group_manager_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.group() & Gates.text("/ban"))
async def ban_user(msg: Message):
    if msg.reply_to_message:
        await app.block_member(msg.chat.id, msg.reply_to_message.sender.id)
        await app.echo(msg, "User banned successfully.")

async def main():
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
