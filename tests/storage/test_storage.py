# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import MemorySession

@pytest.mark.asyncio
async def test_storage_credentials():
    sess = MemorySession("storage_test")
    sess.dc_id = 2
    sess.server_address = "127.0.0.1"
    sess.server_port = 80
    assert sess.dc_id == 2
    assert sess.server_address == "127.0.0.1"
    assert sess.server_port == 80
