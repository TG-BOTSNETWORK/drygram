# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("scheduler_session", api_id=12345, api_hash="abcdef")

async def send_scheduled_alert(chat_id):
    await app.deliver(chat_id=chat_id, text="Scheduled message triggered!")

@app.observe(Gates.text("schedule_me"))
async def schedule_handler(msg: Message):
    await app.dispatcher.scheduler.schedule(
        send_scheduled_alert,
        delay=5.0,
        interval=None,
        chat_id=msg.chat.id
    )
    await app.echo(msg, "Message scheduled in 5 seconds.")

async def main():
    await app.start()
    await asyncio.sleep(8)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
