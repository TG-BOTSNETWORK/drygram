# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_upload_file():
    client = DryClient("test_upload_sess", api_id=1, api_hash="abc")
    await client.start()
    
    cb_calls = []
    def progress_cb(current, total):
        cb_calls.append((current, total))
        
    msg = await client.deliver_file("999", b"filedata", progress_callback=progress_cb)
    assert msg.media is not None
    assert msg.media.file_id == "doc123"
    assert cb_calls == [(100, 100)]
    await client.stop()
