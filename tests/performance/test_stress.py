# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
import pytest
from drygram import DryClient, Gates, Message, User
from drygram.types.chat import Chat
from drygram.sessions.sqlite import SQLiteSession


@pytest.mark.asyncio
async def test_dispatcher_stress_load():
    client = DryClient("stress_dispatcher", api_id=123, api_hash="abc")
    await client.start()

    received_counts = {"count": 0}
    lock = asyncio.Lock()

    @client.observe(Gates.private())
    async def handler(msg: Message):
        async with lock:
            received_counts["count"] += 1

    chat = Chat(id=123, type="private")
    sender = User(id=999, first_name="Sender")
    tasks = []
    
    for i in range(200):
        msg = Message(id=i, date=1000, chat=chat, sender=sender, text=f"message_{i}")
        tasks.append(client.dispatcher.feed_signal(msg))

    await asyncio.gather(*tasks)
    assert received_counts["count"] == 200
    await client.stop()


@pytest.mark.asyncio
async def test_session_concurrency_stress():
    session = SQLiteSession("stress_session_db")
    await session.load()
    session.auth_key = b"S" * 256
    
    async def write_job(idx: int):
        session.user_id = idx
        await session.save()
        
    tasks = [write_job(i) for i in range(100)]
    await asyncio.gather(*tasks)
    
    assert session.user_id == 99
    await session.delete()
