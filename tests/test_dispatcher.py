# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Watcher, Gates, Message, Chat, User
from drygram.dispatch.dispatcher import Dispatcher

@pytest.mark.asyncio
async def test_dispatcher_routing():
    disp = Dispatcher()
    await disp.start()
    
    triggered = []
    
    @disp.register_watcher(Gates.text("hi"))
    async def handler(msg: Message):
        triggered.append(msg.text)
        
    chat = Chat(id=1, type="private")
    sender = User(id=12, first_name="u")
    msg = Message(id=100, date=0, chat=chat, sender=sender, text="hi")
    
    await disp.feed_signal(msg)
    assert triggered == ["hi"]
    
    await disp.stop()
