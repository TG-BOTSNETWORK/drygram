# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_download_file():
    client = DryClient("test_download_sess", api_id=1, api_hash="abc")
    await client.start()
    
    cb_calls = []
    def progress_cb(current, total):
        cb_calls.append((current, total))
        
    data = await client.collect("doc_id", progress_callback=progress_cb)
    assert data == b"mock_file_data"
    assert cb_calls == [(50, 100), (100, 100)]
    await client.stop()
