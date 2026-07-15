# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient, Gates, Message, Chat, User

@pytest.mark.asyncio
async def test_client_login():
    client = DryClient("test_login_session", api_id=1111, api_hash="hash")
    await client.start()
    assert client.me is not None
    assert client.me.id == 12345678
    await client.stop()

@pytest.mark.asyncio
async def test_client_apis():
    client = DryClient("test_apis_sess", api_id=1, api_hash="hash")
    await client.start()
    
    assert await client.request_qr_code() == "tg://login?token=mock_qr_token_12345"
    assert await client.submit_password("pwd") is True
    
    msg = await client.deliver("123", "hello")
    assert msg.text == "hello"
    
    rep = await client.echo(msg, "reply")
    assert rep.text == "reply"
    
    edited = await client.reshape("123", msg.id, "newtext")
    assert edited.text == "newtext"
    
    assert await client.erase("123", msg.id) is True
    
    img = await client.deliver_image("123", b"imgdata", "caption")
    assert img.text == "caption"
    assert img.media.file_id == "photo123"
    
    vid = await client.deliver_video("123", b"viddata", "caption")
    assert vid.text == "caption"
    assert vid.media.file_id == "video123"
    
    rel = await client.relay("123", "456", [1])
    assert rel[0].text == "Forwarded"
    
    dup = await client.duplicate("123", "456", [1])
    assert dup[0].text == "Copied"
    
    assert await client.summon("123") is True
    assert (await client.primitive("123"))["chat_id"] == "123"
    assert await client.anchor("123", 1) is True
    assert await client.release_anchor("123", 1) is True
    assert await client.block_member("123", 1) is True
    assert await client.release_member("123", 1) is True
    assert await client.vault("mykey", "myval") == "myval"
    
    assert await client.publish_story("story") == 999
    
    await client.stop()

def test_gates_evaluation():
    chat = Chat(id=1, type="private")
    sender = User(id=12, first_name="u", is_premium=True)
    msg = Message(id=100, date=0, chat=chat, sender=sender, text="hello")
    
    assert Gates.all_signals()(msg) is True
    assert Gates.text("hello")(msg) is True
    assert Gates.regex(r"he.*")(msg) is True
    assert Gates.private()(msg) is True
    assert Gates.premium()(msg) is True
    assert Gates.sender(12)(msg) is True
    assert Gates.group()(msg) is False
    assert Gates.channel()(msg) is False
    assert Gates.business()(msg) is False
