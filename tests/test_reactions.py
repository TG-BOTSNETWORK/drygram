# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_react_to_story():
    client = DryClient("test_reactions", api_id=1, api_hash="hash")
    await client.start()
    res = await client.react_to_story(999, "👍")
    assert res is True
    await client.stop()
