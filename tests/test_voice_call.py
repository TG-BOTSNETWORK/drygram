# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient, CallParticipant

@pytest.mark.asyncio
async def test_voice_call_lifecycle():
    client = DryClient("test_voice_sess", api_id=1, api_hash="abc")
    await client.start()
    
    await client.enter(999)
    assert client.calls.playing is True
    
    await client.calls.pause(999)
    assert client.calls.playing is False
    
    cb_triggered = []
    client.calls.on_participant_event(lambda p: cb_triggered.append(p))
    
    p = CallParticipant(user_id=123, muted=True)
    await client.calls.trigger_participant_event(p)
    assert len(cb_triggered) == 1
    assert cb_triggered[0].user_id == 123
    
    await client.exit_room(999)
    assert client.calls.playing is False
    await client.stop()
