# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message, InlineKeyboardMarkup, InlineKeyboardButton

app = DryClient("callback_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("menu"))
async def show_menu(msg: Message):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Option 1", callback_data="opt1"),
             InlineKeyboardButton("Option 2", callback_data="opt2")]
        ]
    )
    await app.deliver(chat_id=msg.chat.id, text="Select an option:", markup=inline_kb)

@app.observe(Gates.text("opt1"))
async def handle_callback_opt1(msg: Message):
    await app.echo(msg, "You selected Option 1")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
