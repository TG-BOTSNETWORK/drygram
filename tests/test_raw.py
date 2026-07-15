# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_raw_primitive():
    client = DryClient("test_raw", api_id=1, api_hash="abc")
    await client.start()
    res = await client.primitive("my_chat")
    assert res["chat_id"] == "my_chat"
    assert res["raw_data"] is True
    await client.stop()
