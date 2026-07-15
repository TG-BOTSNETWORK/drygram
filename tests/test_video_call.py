# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_video_call_lifecycle():
    client = DryClient("test_video_sess", api_id=1, api_hash="abc")
    await client.start()
    
    await client.enter(999)
    await client.calls.stream_video(999, "cam.mp4")
    assert client.calls.playing is True
    assert client.calls.current_track == "cam.mp4"
    
    await client.calls.stop_recording()
    assert client.calls.is_recording is False
    
    await client.exit_room(999)
    await client.stop()
