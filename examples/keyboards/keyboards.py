# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

app = DryClient("keyboard_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("keyboards"))
async def send_keyboards(msg: Message):
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Request Contact", request_contact=True)],
            [KeyboardButton("Request Location", request_location=True)]
        ]
    )
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Premium Gift", premium_gift_code="GIFT123")],
            [InlineKeyboardButton("Business Link", business_chat_link="https://t.me/b/123")]
        ]
    )
    await app.deliver(chat_id=msg.chat.id, text="Here is a reply keyboard:", markup=reply_kb)
    await app.deliver(chat_id=msg.chat.id, text="Here is an inline keyboard:", markup=inline_kb)

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
