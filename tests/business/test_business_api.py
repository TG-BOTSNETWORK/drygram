# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_business_settings():
    client = DryClient("test_biz_api", api_id=1, api_hash="abc")
    await client.start()
    assert await client.set_business_greeting("Hi") is True
    assert await client.set_business_away("Offline") is True
    assert await client.set_business_links("link") is True
    await client.stop()
